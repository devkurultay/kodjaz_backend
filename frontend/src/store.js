import { createStore } from 'redux'

import cabinet from './reducers.js'

const store = createStore(cabinet)

export default store
