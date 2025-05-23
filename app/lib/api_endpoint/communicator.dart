import 'dart:async';
import 'dart:convert';

import '/api_endpoint/ble_communication.dart';

class Communicator {
  dynamic challenges;

  Function(dynamic) onMove = (move) {};
  late BLE_Connector _connector;

  Map on = {};

  Communicator(BLE_Connector connector) {
    _connector = connector;
    on['connect'] = (_) {
      print('connect');
    };
    on['disconnect'] = (_) {
      print('disconnected');
    };
    on['error'] = (e) {
      print('Error: $e');
    };
    on['pong'] = (_) {
      print('recieved pong');
    };
    on['status'] = (data) {
      print('data: $data');
    };
    on['move'] = (data) => onMove(data);
    on['challenges'] = (_challenges) {
      challenges = _challenges;
    };
  }
  void emit(String command, dynamic data) async {
    await _connector.sendData(formatData(command, data));
  }

  String formatData(String command, dynamic data) {
    return jsonEncode({"event": "command", "data": jsonEncode(data)});
  }

  void startGame(Map config) {
    // String _config = '{"msg": $config}';
    emit('start_game', config);
  }

  void startStream() {
    emit('start_stream', null);
  }

  void checkForMove() {
    emit('check', null);
  }

  void getLichessChallenges() {
    emit('challenges', null);
  }

  void startOnlineGame(config) {
    emit('start_lichess', config);
  }

  void handleCommand(command, data) {
    try {
      on[command](command, data);
    } catch (e) {
      print('undefined command');
    }
  }
}
