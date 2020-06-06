import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import {
  loadTracks,
  resetNewlyCreatedLessonId
} from '../../actions/entity'
import {
  logout
} from '../../actions/login'

import Cabinet from './Cabinet'

const mapStateToProps = (state) => ({})

const mapDispatchToProps = (dispatch) => {
  return bindActionCreators({
    logout,
    loadTracks,
    resetNewlyCreatedLessonId
  }, dispatch)
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Cabinet)
