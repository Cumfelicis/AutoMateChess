import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_reactive_ble/flutter_reactive_ble.dart';
import 'package:permission_handler/permission_handler.dart';

class BLE_Connector {
  final FlutterReactiveBle _ble = FlutterReactiveBle();
  final Completer<void> _readyCompleter = Completer<void>();
  late final StreamSubscription<DiscoveredDevice> _scanstream;
  late StreamSubscription<ConnectionStateUpdate> _connectionStream;
  late QualifiedCharacteristic _rxCharacteristic;
  late QualifiedCharacteristic _txCharacteristic;
  late QualifiedCharacteristic notifyCharacteristic;
  late DiscoveredDevice _device;
  final Uuid SERVICE_UUID = Uuid.parse("12345678-1234-5678-1234-56789abcdef0");

  final Uuid RX_CHAR_UUID = Uuid.parse("0000abcd-0000-1000-8000-00805f9b34fb");

  final Uuid TX_CHAR_UUID = Uuid.parse("0000abcd-0000-1000-8000-00805f9b34fb");

  final CHAR_UUID = Uuid.parse("abcd");

  Future<void> requestBlePermissions() async {
    if (await Permission.location.isDenied) {
      await Permission.location.request();
    }
    if (await Permission.bluetoothScan.request() != PermissionStatus.granted) {
      throw Exception('Bluetooth scan permission not granted');
    }

    if (await Permission.bluetoothConnect.request() !=
        PermissionStatus.granted) {
      throw Exception('Bluetooth connect permission not granted');
    }
  }

  Future<void> startScanning() async {
    await requestBlePermissions();
    _scanstream = _ble.scanForDevices(
      withServices: [], // or your advertised service UUID
      scanMode: ScanMode.lowLatency,
    ).listen((device) {
      if (device.name == "GopherReceiver") {
        print("Found device: ${device.id}");
        _device = device;
        _scanstream.cancel();
        connectToDevice(device);
      } else {
        print('test');
      }
    });
  }

  void connectToDevice(DiscoveredDevice device) async {
    _connectionStream =
        _ble.connectToDevice(id: device.id).listen((connectionState) {
      print(connectionState.connectionState);
      if (connectionState.connectionState == DeviceConnectionState.connected) {
        print('connected to device: $device.id');

        notifyCharacteristic = QualifiedCharacteristic(
          serviceId: SERVICE_UUID,
          characteristicId: CHAR_UUID,
          deviceId: device.id,
        );
        _ble.subscribeToCharacteristic(notifyCharacteristic).listen((data) {
          print("Notification from server: ${String.fromCharCodes(data)}");
        });
        _readyCompleter.complete();
      } else if (connectionState.connectionState ==
          DeviceConnectionState.disconnected) {
        print('disconnected');
      }
    });
  }

  Future<void> sendData(String data) async {
    try {
      await _ble.writeCharacteristicWithoutResponse(
          QualifiedCharacteristic(
              characteristicId: RX_CHAR_UUID,
              serviceId: SERVICE_UUID,
              deviceId: _device.id),
          value: data.codeUnits);
      print('Data sent: $data');
    } catch (e) {
      print('Error writing: $e');
    }
  }

  Future<void> get onReady => _readyCompleter.future;
}

final CONNECTOR = BLE_Connector();
