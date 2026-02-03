using FellowOakDicom;
using FellowOakDicom.Network;
using System.Text;

namespace MwlBroker.Service;

public class Worker : BackgroundService
{
    private readonly ILogger<Worker> _logger;
    private IDicomServer? _dicomServer;
    private const int Port = 11112;
    private const string AeTitle = "MWLBROKER";

    public Worker(ILogger<Worker> logger)
    {
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        try
        {
            _logger.LogInformation("Starting DICOM C-ECHO SCP on port {Port} with AE Title {AeTitle}", Port, AeTitle);
            
            _dicomServer = DicomServerFactory.Create<EchoService>(Port);
            
            _logger.LogInformation("DICOM C-ECHO SCP started successfully on port {Port}", Port);
            
            // Keep the service running
            while (!stoppingToken.IsCancellationRequested)
            {
                await Task.Delay(1000, stoppingToken);
            }
        }
        catch (OperationCanceledException)
        {
            // Expected when service is stopping
            _logger.LogInformation("Service stopping");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error in DICOM SCP service");
            throw;
        }
    }

    public override Task StopAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("Stopping DICOM C-ECHO SCP");
        _dicomServer?.Dispose();
        return base.StopAsync(cancellationToken);
    }
}

public class EchoService : DicomService, IDicomServiceProvider, IDicomCEchoProvider
{
    public EchoService(INetworkStream stream, Encoding fallbackEncoding, ILogger logger, DicomServiceDependencies dependencies)
        : base(stream, fallbackEncoding, logger, dependencies)
    {
    }

    public Task OnReceiveAssociationRequestAsync(DicomAssociation association)
    {
        Logger.LogInformation("Received association request from {CallingAE}", association.CallingAE);
        
        foreach (var pc in association.PresentationContexts)
        {
            pc.SetResult(DicomPresentationContextResult.Accept);
        }
        
        return SendAssociationAcceptAsync(association);
    }

    public Task OnReceiveAssociationReleaseRequestAsync()
    {
        Logger.LogInformation("Received association release request");
        return SendAssociationReleaseResponseAsync();
    }

    public void OnReceiveAbort(DicomAbortSource source, DicomAbortReason reason)
    {
        Logger.LogWarning("Association aborted: {Source} - {Reason}", source, reason);
    }

    public void OnConnectionClosed(Exception exception)
    {
        if (exception != null)
        {
            Logger.LogError(exception, "Connection closed with error");
        }
        else
        {
            Logger.LogInformation("Connection closed");
        }
    }

    public Task<DicomCEchoResponse> OnCEchoRequestAsync(DicomCEchoRequest request)
    {
        Logger.LogInformation("Received C-ECHO request");
        return Task.FromResult(new DicomCEchoResponse(request, DicomStatus.Success));
    }
}
