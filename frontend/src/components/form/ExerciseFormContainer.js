import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import ExerciseForm from './ExerciseForm'

import { loadExercise } from '../../actions/entity'

const mapStateToProps = (state) => {
  return {
    currentExercise: state.currentExercise
  }
}

const mapDispatchToProps = (dispatch) => {
  return bindActionCreators(
    { loadExercise },
    dispatch
  )
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(ExerciseForm)
