import 'package:auto_mate_chess/components/utils/responsive_utils.dart';
import 'package:flutter/material.dart';

class ResponsiveText extends Text {
  const ResponsiveText(
    super.data, {
    super.key,
    TextStyle super.style = const TextStyle(fontSize: 12.0),
    super.textAlign,
    super.textDirection,
    super.locale,
    super.softWrap,
    super.overflow,
    super.textScaler,
    super.maxLines,
    super.semanticsLabel,
    super.textWidthBasis,
  });

  @override
  Widget build(BuildContext context) {
    return Text(
      data!,
      key: key,
      style:
          style!.copyWith(fontSize: responsiveWidth(style!.fontSize!, context)),
      textAlign: textAlign,
      textDirection: textDirection,
      locale: locale,
      softWrap: softWrap,
      overflow: overflow,
      textScaler: textScaler,
      maxLines: maxLines,
      semanticsLabel: semanticsLabel,
      textWidthBasis: textWidthBasis,
    );
  }
}
