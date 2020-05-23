import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import { loadTracks } from '../../actions/entity'

import Tree from './Tree'

const mapStateToProps = (state) => {
  return {
    tracks: state.tracks,
    isLoadTracksPending: state.isLoadTracksPending
  }
}

const mapDispatchToProps = (dispatch) => {
  return bindActionCreators({ loadTracks }, dispatch)
}

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Tree)
