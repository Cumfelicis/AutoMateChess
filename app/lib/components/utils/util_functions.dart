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
