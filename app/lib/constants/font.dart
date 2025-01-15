import 'package:flutter/material.dart';

import 'tint.dart';

class Font {
  static TextStyle h1 = const TextStyle(
      fontSize: 20, color: Tint.background, fontWeight: FontWeight.w700);

  static TextStyle body1 = const TextStyle(
      fontSize: 15, color: Tint.background, fontWeight: FontWeight.w500);
  static TextStyle body1Primary = const TextStyle(
      fontSize: 15, color: Tint.primary, fontWeight: FontWeight.w500);
}
