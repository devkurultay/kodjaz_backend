const initialState = {
  isAuthenticated: null,
  loginError: [],
  currentExercise: {},
  entityLoadingError: '',
  isLoadTracksPending: false,
  isLoadLessonsPending: false,
  isLoadExercisesPending: false,
  isSaveTrackPending: false,
  tracks: [],
  lessons: [],
  exercises: [],
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
    case 'LOAD_EXERCISES_PENDING':
      return {
        ...state,
        isLoadExercisesPending: true
      }
    case 'LOAD_EXERCISES_FULFILLED':
      return {
        ...state,
        isLoadExercisesPending: false,
        exercises: action.payload.data
      }
    case 'SAVE_TRACK_PENDING':
      return {
        ...state,
        isSaveTrackPending: true
      }
    case 'SAVE_TRACK_FULFILLED':
      const updatedTrack = action.payload.data
      const tracks = state.tracks.reduce((acc, tr, ind) => {
        if (tr.id === updatedTrack.id) {
          acc.push(updatedTrack)
        } else {
          acc.push(tr)
        }
        return acc
      }, [])
      return {
        ...state,
        isSaveTrackPending: false,
        tracks
      }
    default:
      return state
  }
}

export default cabinet
