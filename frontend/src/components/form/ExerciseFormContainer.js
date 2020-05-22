import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import ExerciseForm from './ExerciseForm'

import {
  loadExercise,
  loadLessons,
  saveExercise
} from '../../actions/entity'

const mapStateToProps = (state) => {
  return {
    lessons: state.lessons,
    currentExercise: state.currentExercise
  }
}

const mapDispatchToProps = (dispatch) => {
  return bindActionCreators({
    loadExercise,
    loadLessons,
    saveExercise
  }, dispatch)
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(ExerciseForm)
