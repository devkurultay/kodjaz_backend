import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import {
  loadTracks,
  resetNewlyCreatedLessonId
} from '../../actions/entity'

import Cabinet from './Cabinet'

const mapStateToProps = (state) => ({})

const mapDispatchToProps = (dispatch) => {
  return bindActionCreators({
    loadTracks,
    resetNewlyCreatedLessonId
  }, dispatch)
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Cabinet)
