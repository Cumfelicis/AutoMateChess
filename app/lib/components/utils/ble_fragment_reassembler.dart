import 'dart:convert';

import 'package:auto_mate_chess/api_endpoint/communicator.dart';

class BleMessageReassembler {
  final Map<int, List<int>> _chunks = {};
  int? _expectedChunks;
  late final _communicator;

  BleMessageReassembler(Communicator communicator) {
    _communicator = communicator;
  }

  void handleIncomingData(List<int> data) {
    if (data.length < 3) {
      print("Invalid data (too short): $data");
      return;
    }

    final index = data[0];
    final total = data[1];
    final payloadLength = data[2];

    if (data.length < 3 + payloadLength) {
      print("Invalid data (payload length mismatch): $data");
      return;
    }

    final payload = data.sublist(3, 3 + payloadLength);

    _expectedChunks ??= total;

    _chunks[index] = payload;

    print("Received chunk ${index + 1}/$total: ${utf8.decode(payload)}");

    if (_chunks.length == _expectedChunks) {
      _assembleMessage();
    }
  }

  void _assembleMessage() {
    final fullData = <int>[];
    for (int i = 0; i < _expectedChunks!; i++) {
      final chunk = _chunks[i];
      if (chunk == null) {
        print("Missing chunk $i, cannot reassemble.");
        return;
      }
      fullData.addAll(chunk);
    }

    final message = jsonDecode(utf8.decode(fullData));
    print("? Full message reassembled: $message");
    _communicator.handleCommand(message["event"], message["data"]);

    // Reset state for next message
    _chunks.clear();
    _expectedChunks = null;
  }
}
