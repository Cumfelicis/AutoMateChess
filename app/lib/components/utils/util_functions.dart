import 'package:flutter/material.dart';

import '../commons/chess_board/piece.dart';

bool isNumeric(String? str) {
  if (str == null) {
    return false;
  }
  return num.tryParse(str) != null;
}

void preCacheImages(BuildContext context) {
  for (final path in images.values) {
    precacheImage(AssetImage(path), context);
  }
}

Map createGameConfig(bool color, String setup, bool humanTime, bool ontime,
    int startingTime, int increment) {
  return {
    'color': color,
    'fen': setup, // starting position in FEN format
    'human_time': humanTime,
    'on_time': ontime,
    'starting_time': startingTime,
    'increment': increment
  };
}
