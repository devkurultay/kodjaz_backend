import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import {
  saveTrack,
  saveUnit,
  saveLesson,
  createTrack,
  createUnit,
} from '../../actions/entity'

import Tree from './Tree'

const mapStateToProps = (state) => {
  return {
    tracks: state.tracks,
    isLoadTracksPending: state.isLoadTracksPending,
    isSaveTrackPending: state.isSaveTrackPending
  }
}

const mapDispatchToProps = (dispatch) => {
  return bindActionCreators({
    saveTrack,
    saveUnit,
    saveLesson,
    createTrack,
    createUnit,
  }, dispatch)
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Tree)
