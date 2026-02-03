# MwlBroker Service

A minimal .NET 8 DICOM C-ECHO SCP (Service Class Provider) using fo-dicom 5.x.

## Features

- DICOM C-ECHO SCP listening on port 11112
- AE Title: MWLBROKER
- Serilog logging to console and rolling file logs (logs/service-.log)
- Built with FellowOakDicom 5.1.3

## Building

```bash
dotnet build
```

## Running

```bash
dotnet run
```

The service will start listening on port 11112 for DICOM C-ECHO requests.

## Testing

Use DCMTK's echoscu to test the service:

```bash
echoscu localhost 11112
```

Or with a custom calling AE title:

```bash
echoscu -aec CUSTOM_AE localhost 11112
```

## Logs

Logs are written to:
- Console (stdout)
- Rolling file: `logs/service-YYYYMMDD.log`

## Dependencies

- .NET 8.0
- fo-dicom 5.1.3
- Serilog.Extensions.Hosting 10.0.0
- Serilog.Sinks.File 7.0.0
- Serilog.Sinks.Console 6.1.1
