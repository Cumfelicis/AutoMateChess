import 'package:auto_mate_chess/constants/tint.dart';
import 'package:flutter/material.dart';

class StandardFab extends StatelessWidget {
  final Widget child;
  final Function() onPressed;
  final Color? backgroundColor;
  final String? herotag;
  const StandardFab({
    super.key,
    required this.onPressed,
    required this.child,
    this.backgroundColor,
    this.herotag,
  });

  @override
  Widget build(BuildContext context) {
    return FloatingActionButton(
      heroTag: herotag,
      backgroundColor: backgroundColor ?? Tint.background,
      onPressed: onPressed,
      child: child,
    );
  }
}
