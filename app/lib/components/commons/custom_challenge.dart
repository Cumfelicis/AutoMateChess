import 'package:auto_mate_chess/components/utils/responsive_text.dart';
import 'package:flutter/material.dart';

import '../../constants/font.dart';
import '../../constants/tint.dart';
import '../utils/responsive_utils.dart';

class CustomChallenge extends StatelessWidget {
  const CustomChallenge({super.key});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
        child: Padding(
      padding: EdgeInsets.all(responsiveHeight(5, context)),
      child: SizedBox(
        height: responsiveHeight(65, context),
        width: responsiveWidth(65, context),
        child: Container(
          decoration: const BoxDecoration(
            color: Tint.primary,
            boxShadow: [BoxShadow()],
            borderRadius: BorderRadius.all(
              Radius.circular(5),
            ),
          ),
          child: ResponsiveText(
            'Other',
            style: Font.h1,
          ),
        ),
      ),
    ));
  }
}
