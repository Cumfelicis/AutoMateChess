import 'dart:async';
import 'dart:io';

import 'package:socket_io_client/socket_io_client.dart' as IO;

class WebSocket {
  IO.Socket socket = IO.io('http://172.20.10.4:5000', <String, dynamic>{
    'transports': ['websocket'],
    'reconnect': true,
    'reconnectDelay': 5000,
    'reconnectAttempts': 10
  });
  dynamic challenges;

  Function(dynamic) onMove = (move) {};
  WebSocket() {
    socket.onConnect((_) {
      socket.emit('command', 'connected');
      Timer.periodic(Duration(seconds: 30), (timer) {
        if (socket.connected) {
          print('emitted ping');
          socket.emit('ping',
              'ping'); // send messages periodicly to keep connection to websocket alive
        }
      });
    });
    socket.onDisconnect((_) {
      print('disconnected');
    });
    socket.onError((e) {
      print('Error: $e');
    });
    socket.on(
      'pong',
      (_) => print('recieved pong'),
    );
    socket.on(
      'status',
      (data) => print(data),
    );
    socket.on('move', (data) => onMove(data));
    socket.on('challenges', (_challenges) => challenges = _challenges);
    // Set up a periodic timer to send a ping message every 30 second
  }

  void startGame(Map config) {
    // String _config = '{"msg": $config}';
    socket.emit('start_game', config);
  }

  void startStream() {
    socket.emit('start_stream');
  }

  void checkForMove() {
    socket.emit('check');
  }

  void getLichessChallenges() {
    socket.emit('challenges');
  }

  void startOnlineGame(config) {
    socket.emit('start_lichess', config);
  }
}

WebSocket SOCKET = WebSocket();
