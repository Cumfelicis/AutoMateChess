import 'package:flutter/material.dart';

double responsiveWidth(double width, BuildContext context,
    {double reference = 392.7}) {
  double deviceWidth = MediaQuery.of(context).size.width;
  double factor = width / reference;
  return deviceWidth * factor;
}

double responsiveHeight(double height, BuildContext context,
    {double reference = 781.1}) {
  double deviceHeight = MediaQuery.of(context).size.height;
  double factor = height / reference;
  return deviceHeight * factor;
}
