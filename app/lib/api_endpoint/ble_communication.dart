import 'dart:async';
import 'dart:convert';

import 'package:auto_mate_chess/components/utils/ble_fragment_reassembler.dart';
import 'package:flutter/material.dart';
import 'package:flutter_reactive_ble/flutter_reactive_ble.dart';
import 'package:permission_handler/permission_handler.dart';

class BLE_Connector {
  final FlutterReactiveBle _ble = FlutterReactiveBle();
  final Completer<void> _readyCompleter = Completer<void>();
  final _reassembler = BleMessageReassembler();
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
          _reassembler.handleIncomingData(data);
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

  Future<void> sendFragmentedMessage(String message) async {
    final data = utf8.encode(message);
    const maxPayload = 17; // 20 - 3 bytes for metadata
    final totalChunks = (data.length / maxPayload).ceil();
    if (totalChunks > 255) {
      print("Message too long");
      return;
    }

    for (int i = 0; i < totalChunks; i++) {
      final start = i * maxPayload;
      final end =
          (start + maxPayload > data.length) ? data.length : start + maxPayload;
      final payload = data.sublist(start, end);

      final chunk = [
        i, // chunk number
        totalChunks, // total number of chunks
        payload.length, // actual payload length
        ...payload
      ];

      await _ble.writeCharacteristicWithoutResponse(
          QualifiedCharacteristic(
              characteristicId: RX_CHAR_UUID,
              serviceId: SERVICE_UUID,
              deviceId: _device.id),
          value: chunk);
      await Future.delayed(const Duration(milliseconds: 50)); // pacing
    }
  }

  Future<void> get onReady => _readyCompleter.future;
}

final CONNECTOR = BLE_Connector();
