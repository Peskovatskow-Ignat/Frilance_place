$mq-breakpoints: (tn: 384, xxs: 480, xs: 576, sm: 768, md: 992,
        lg: 1200, xl: 1400, xxl: 1920, xxxl: 3000, max: 100000);

@function breakpoint-max($name, $breakpoints: $mq-breakpoints) {
  $max: map-get($breakpoints, $name);
  @return if($max and $max > 0, $max - 1, null);
}

@function breakpoint-min($name, $breakpoints: $mq-breakpoints) {
  $min: map-get($breakpoints, $name);
  @return if($min != 0, $min, null);
}

@mixin tn {
  $max: breakpoint-max(tn, $mq-breakpoints);
  @media(max-width: #{$max}px) {
    @content;
  }
}

@mixin xxs {
  $max: breakpoint-max(xxs, $mq-breakpoints);
  @media(max-width: #{$max}px) {
    @content;
  }
}

@mixin xs {
  $max: breakpoint-max(xs, $mq-breakpoints);
  @media(max-width: #{$max}px) {
    @content;
  }
}

@mixin sm {
  $max: breakpoint-max(sm, $mq-breakpoints);
  @media(max-width: #{$max}px) {
    @content;
  }
}

@mixin md {
  $max: breakpoint-max(md, $mq-breakpoints);
  @media(max-width: #{$max}px) {
    @content;
  }
}

@mixin lg {
  $max: breakpoint-max(lg, $mq-breakpoints);
  @media(max-width: #{$max}px) {
    @content;
  }
}

@mixin xl {
  $max: breakpoint-max(xl, $mq-breakpoints);
  @media(max-width: #{$max}px) {
    @content;
  }
}

@mixin xxl {
  $max: breakpoint-max(xxl, $mq-breakpoints);
  @media(max-width: #{$max}px) {
    @content;
  }
}

@mixin xxxl {
  $max: breakpoint-max(xxxl, $mq-breakpoints);
  @media(max-width: #{$max}px) {
    @content;
  }
}

@mixin max {
  $max: breakpoint-max(max, $mq-breakpoints);
  @media(max-width: #{$max}px) {
    @content;
  }
}

@mixin mq-down($name, $breakpoints: $mq-breakpoints) {
  $max: breakpoint-max($name, $breakpoints);
  @if $max {
    @media (max-width: #{$max}px) {
      @content;
    }
  } @else {
    @content;
  }
}

@mixin mq-between($lower, $upper, $breakpoints: $mq-breakpoints) {
  $min: breakpoint-min($lower, $breakpoints);
  $max: breakpoint-max($upper, $breakpoints);

  @media (min-width: #{$min}px) and (max-width: #{$max}px) {
    @content;
  }
}

@mixin h-center-content {
  display: flex;
  justify-content: center;
}

@mixin v-center-content {
  display: flex;
  align-items: center;
}

@mixin center-content {
  display: flex;
  justify-content: center;
  align-items: center;
}

@mixin flex-column {
  display: flex;
  flex-direction: column;
}

@mixin flex-item($grow: 0, $shrink: 1, $basis: auto) {
  display: flex;
  position: relative;
  flex: $grow $shrink $basis;
}

@mixin font-face($font, $color, $letterSpacing: 0px) {
  font: $font;
  color: $color;
  letter-spacing: $letterSpacing;
}