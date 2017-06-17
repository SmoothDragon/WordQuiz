import React from 'react';
import { Button, Image, StyleSheet, Text, TouchableOpacity, View } from 'react-native';


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontFamily: 'monospace',
    fontSize: 20,
  },
  row:{
      flexDirection:'row',
  },
  AnswerBox:{
    height: 80,
    width: 300,
    alignItems: 'center',
    justifyContent: 'center',
    borderColor: 'white',
    borderWidth: 2,
  },
  AnswerBoxText: {
    fontFamily: 'monospace',
    fontSize: 50,
    fontWeight: 'bold',
    color: 'white',
  },
  QuestionBoxText: {
    fontFamily: 'monospace',
    fontSize: 40,
    fontWeight: 'bold',
    color: 'black',
  },
});


function AnswerBox(props) {
    return (
      <TouchableOpacity
        style={[styles.AnswerBox, {backgroundColor: props.bgColor}]}
        onPress={props.onPress}>
          <Text style={styles.AnswerBoxText}>{props.text}</Text>
      </TouchableOpacity>
    );
}

function QuestionBox(props) {
  return (
    <Text
      style={[styles.QuestionBoxText, {color: props.color}]}>
      {props.word}
    </Text>
  );
}

function WordInfo() {
  return ({
    quizOrder: ['CAT', 'FOC', 'BIZ'],
    wordValid: {
    'CAT': true,
    'BIZ': true,
    'FOC': false,
    },
  });
}

export default class WordQuiz extends React.Component {
  constructor() {
    super();
    wordInfo = WordInfo();
    this.state = {
      wordValid: wordInfo.wordValid,
      quizOrder: wordInfo.quizOrder,
      currentColor: 'black',
      pos: 0,
    }
  }
 
  handlePress(bool) {
    const word = this.state.quizOrder[this.state.pos];
    if (this.state.wordValid[word] == bool) {
      this.setState({
        pos: (this.state.pos + 1) % this.state.quizOrder.length,
        currentColor: 'black',
      });
    } else {
      this.setState({
        currentColor: this.state.wordValid[word] ? 'green' : 'red',
      });
    }
    return;
  }

  render() {
    return (
      <View style={styles.container}>
        <View>
        </View>
        <QuestionBox 
          color={this.state.currentColor} 
          word={this.state.quizOrder[this.state.pos]}
        />
        <AnswerBox bgColor='green' text='YES' onPress={() => this.handlePress(true)}/>
        <AnswerBox bgColor='red' text='NO' onPress={() => this.handlePress(false)}/>
      </View>
    );
  }
}


