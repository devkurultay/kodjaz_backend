const initialState = {
  isAuthenticated: null,
  loginError: [],
  currentExercise: {},
  entityLoadingError: '',
  isLoadTracksPending: false,
  isLoadLessonsPending: false,
  tracks: [],
  lessons: [],
}

function cabinet(state = initialState, action) {
  switch(action.type) {
    case 'LOG_IN':
      return {
        ...state,
        loginError: [],
        isAuthenticated: true
      }
    case 'FAILED_TO_LOG_IN':
      return {
        ...state,
        isAuthenticated: false,
        loginError: action.payload
      }
    case 'LOAD_EXERCISE':
      return {
        ...state,
        entityLoadingError: '',
        currentExercise: action.payload
      }
    case 'FAILED_TO_LOAD':
      return {
        ...state,
        entityLoadingError: action.payload
      }
    case 'LOAD_TRACKS_PENDING':
      return {
        ...state,
        isLoadTracksPending: true
      }
    case 'LOAD_TRACKS_FULFILLED':
      return {
        ...state,
        isLoadTracksPending: false,
        tracks: action.payload.data
      }
    case 'LOAD_LESSONS_PENDING':
      return {
        ...state,
        isLoadLessonsPending: true
      }
    case 'LOAD_LESSONS_FULFILLED':
      return {
        ...state,
        isLoadLessonsPending: false,
        lessons: action.payload.data
      }
    default:
      return state
  }
}

export default cabinet
