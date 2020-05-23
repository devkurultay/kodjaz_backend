import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import { loadTracks } from '../../actions/entity'

import Cabinet from './Cabinet'

const mapStateToProps = (state) => ({})

const mapDispatchToProps = (dispatch) => {
  return bindActionCreators({ loadTracks }, dispatch)
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Cabinet)
