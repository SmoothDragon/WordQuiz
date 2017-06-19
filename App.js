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

function WordInfo2() {
  return [{'timestamp': 1497712078.1578422, 'cardbox': 1, 'dict': 'OWL14', 'name': 'SYN', 'isWord': 1}, {'timestamp': 1497712081.3843472, 'cardbox': 1, 'dict': 'OWL14', 'name': 'REA', 'isWord': 0}, {'timestamp': 1497712083.3533807, 'cardbox': 2, 'dict': 'OWL14', 'name': 'AJE', 'isWord': 0}, {'timestamp': 1497712084.2478843, 'cardbox': 2, 'dict': 'OWL14', 'name': 'VAI', 'isWord': 0}, {'timestamp': 1497712088.6850865, 'cardbox': 2, 'dict': 'OWL14', 'name': 'VIT', 'isWord': 0}, {'timestamp': 1497712090.5375645, 'cardbox': 2, 'dict': 'OWL14', 'name': 'CAM', 'isWord': 1}, {'timestamp': 1497712091.5030003, 'cardbox': 2, 'dict': 'OWL14', 'name': 'KIT', 'isWord': 1}, {'timestamp': 1497712092.168156, 'cardbox': 7, 'dict': 'OWL14', 'name': 'TWO', 'isWord': 1}, {'timestamp': 1497712093.2779875, 'cardbox': 8, 'dict': 'OWL14', 'name': 'SAA', 'isWord': 0}, {'timestamp': 1497712094.9799373, 'cardbox': 8, 'dict': 'OWL14', 'name': 'RHY', 'isWord': 0}];
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
    const milliseconds = (new Date).getTime();
    console.log(milliseconds);
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

  async fetchData() {
    try {
      let response = await fetch('http://50.114.241.53/json');
      let responseJSON = await response.json();
      console.log(responseJSON);
      this.setState({
        wordValid: responseJSON.wordValid,
        quizOrder: responseJSON.quizOrder,
      });
    } catch(error) {
      console.error(error);
    }
  }

  async fetchData2() {
    try {
      let response = await fetch('http://50.114.241.53/quiz');
      let responseJSON = await response.json();
      console.log(responseJSON);
      this.setState({
        quiz: response.JSON,
        wordValid: responseJSON.wordValid,
        quizOrder: responseJSON.quizOrder,
      });
    } catch(error) {
      console.error(error);
    }
  }

  componentDidMount() {
    this.fetchData().done()
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


