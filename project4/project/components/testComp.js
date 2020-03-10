import React from 'react';
import {
  SafeAreaView,
  StyleSheet,
  ScrollView,
  View,
  Text,
  StatusBar,
} from 'react-native';

export const ManoKomponentas = ({tekstas}) => {
  return (
    <>
      <Text style={{color: 'red',fontWeight: 'bold' ,marginTop: '50%' ,marginLeft: '40%'}}>
      As einu gatve
      </Text>
    </>
  )
}

export const Headeris = () => {
  return (
    <>
    <View style={{backgroundColor: 'blue' ,height: '20%' ,width:'100%', position: 'absolute' ,top: '0'}}></View>
    </>
  )
}
