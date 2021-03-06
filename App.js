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
  DefinitionBox:{
    height: 200,
    width: 300,
    alignItems: 'center',
    justifyContent: 'center',
    borderColor: 'white',
    borderWidth: 2,
  },
  DefinitionBoxText: {
    fontFamily: 'monospace',
    fontSize: 20,
    color: 'black',
  },
});


function DefinitionBox(props) {
    return (
      <TouchableOpacity
        style={[styles.DefinitionBox, {backgroundColor: props.bgColor}]}>
          <Text style={styles.DefinitionBoxText}>
            {props.text}
          </Text>
      </TouchableOpacity>
    );
}

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
  const size = ~~(24/props.word.length) * 10; // Smaller font for larger words
  return (
    <Text
      style={[styles.QuestionBoxText, {color: props.color, fontSize: size}]}
      onPress={props.onPress}>
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
    this.state = {
      quiz: WordInfo2(),
      currentColor: 'black',
      pos: 0,
      defintion: '',
    }
  }
 
  handlePress(bool) {
    const milliseconds = (new Date).getTime();
    console.log(milliseconds);
    const current = this.state.quiz[this.state.pos];
    const word = current.word;
    if (current.isWord == bool) {
      this.setState({
        pos: (this.state.pos + 1) % this.state.quiz.length,
        currentColor: 'black',
        definition: '',
      });
    } else {
      this.setState({
        currentColor: current.isWord ? 'green' : 'red',
        definition: current.definition,
      });
    }
    return;
  }

  handleQuestionPress() {
    const current = this.state.quiz[this.state.pos];
    this.setState({
      currentColor: 'black',
      definition: current.definition,
    });
    return;
  }


  async fetchData() {
    try {
      let response = await fetch('http://50.114.241.53/quiz');
      let responseJSON = await response.json();
      console.log(responseJSON);
      this.setState({
        quiz: responseJSON.quiz,
      });
    } catch(error) {
      console.error(error);
    }
  }

  componentDidMount() {
    this.fetchData().done()
  }

  render() {
    const current = this.state.quiz[this.state.pos];
    return (
      <View style={styles.container}>
        <View>
        </View>
        <DefinitionBox text={this.state.definition} />
        <QuestionBox 
          color={this.state.currentColor} 
          word={current.name}
          onPress={() => this.handleQuestionPress()}
        />
        <AnswerBox bgColor='green' text='YES' onPress={() => this.handlePress(1)}/>
        <AnswerBox bgColor='red' text='NO' onPress={() => this.handlePress(0)}/>
      </View>
    );
  }
}


