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

export default connect(
  mapStateToProps
)(Tree)
