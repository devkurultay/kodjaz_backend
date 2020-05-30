import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import ExerciseForm from './ExerciseForm'

import {
  loadExercises,
  loadLessons,
  saveExercise,
  createExercise
} from '../../actions/entity'

const mapStateToProps = (state) => {
  return {
    tracks: state.tracks,
    lessons: state.lessons,
    exercises: state.exercises,
    isSaveExercisePending: state.isSaveExercisePending,
    saveExerciseError: state.saveExerciseError,
  }
}

const mapDispatchToProps = (dispatch) => {
  return bindActionCreators({
    loadExercises,
    loadLessons,
    saveExercise,
    createExercise
  }, dispatch)
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(ExerciseForm)
