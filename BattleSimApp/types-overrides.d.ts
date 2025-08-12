declare module '@react-native-community/slider' {
  import { Component } from 'react';
  import { ViewProps } from 'react-native';

  export interface SliderProps extends ViewProps {
    value?: number;
    minimumValue?: number;
    maximumValue?: number;
    step?: number;
    minimumTrackTintColor?: string;
    maximumTrackTintColor?: string;
    thumbTintColor?: string;
    disabled?: boolean;
    onValueChange?: (value: number) => void;
    onSlidingComplete?: (value: number) => void;
  }

  export default class Slider extends Component<SliderProps> {}
}


// Victory Native type shim: map to 'victory' exports so TS recognizes components
declare module 'victory-native' {
  export * from 'victory';
}

