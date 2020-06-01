const initialState = {
  isAuthenticated: null,
  loginError: [],
  currentExercise: {},
  entityLoadingError: '',
  isLoadTracksPending: false,
  isLoadLessonsPending: false,
  isLoadExercisesPending: false,
  isSaveTrackPending: false,
  isSaveUnitPending: false,
  isSaveLessonPending: false,
  isSaveExercisePending: false,
  saveExerciseError: {},
  tracks: [],
  lessons: [],
  exercises: [],
  newlyCreatedExerciseId: null,
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
    case 'SAVE_UNIT_PENDING':
      return {
        ...state,
        isSaveUnitPending: true
      }
    case 'SAVE_LESSON_PENDING':
      return {
        ...state,
        isSaveLessonPending: true
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
    case 'SAVE_UNIT_FULFILLED':
      const updatedUnit = action.payload.data
      const updatedTracks = state.tracks.reduce((acc, tr) => {
        // Identify a track by the update unit's track id
        if (tr.id === updatedUnit.track) {
          const updatedTrackUnits = tr.track_units.reduce((units, un) => {
            // Identify the unit by the updated unit's id
            if (un.id === updatedUnit.id) {
              // Put the updated unit
              units.push(updatedUnit)
            } else {
              units.push(un)
            }
            return units
          }, [])
          // Update the track's units list
          tr.track_units = updatedTrackUnits
          // ... and put it to the new list of tracks
          acc.push(tr)
        } else {
          // Put non-affected tracks intact
          acc.push(tr)
        }
        return acc
      }, [])
      return {
        ...state,
        isSaveUnitPending: false,
        tracks: updatedTracks
      }
    case 'SAVE_LESSON_FULFILLED':
      const updatedLesson = action.payload.data
      const updatedTrs = state.tracks.reduce((tracks, tr, idx) => {
        // Try to update each track's unit's lessons
        const updUnits = tr.track_units.reduce((acc, un) => {
          // Get the lesson's unit by id
          if (un.id === updatedLesson.unit) {
            // Update unit's lessons
            const updatedLessons = un.unit_lessons.reduce((acc, les) => {
              if (les.id === updatedLesson.id) {
                acc.push(updatedLesson)
              } else {
                acc.push(les)
              }
              return acc
            }, [])
            un.unit_lessons = updatedLessons
            acc.push(un)
          } else {
            acc.push(un)
          }
          return acc
        }, [])
        tr.track_units = updUnits
        tracks.push(tr)
        return tracks
      }, [])
      return {
        ...state,
        tracks: updatedTrs
      }
    case 'SAVE_EXERCISE_PENDING':
      return {
        ...state,
        isSaveExercisePending: true,
        saveExerciseError: {},
      }
    case 'SAVE_EXERCISE_FULFILLED':
      const updatedExercise = action.payload.data
      const exercises = state.exercises.reduce((acc, ex, ind) => {
        if (ex.id === updatedExercise.id) {
          acc.push(updatedExercise)
        } else {
          acc.push(ex)
        }
        return acc
      }, [])
      return {
        ...state,
        isSaveExercisePending: false,
        exercises
      }
    case 'SAVE_EXERCISE_ERROR':
      return {
        ...state,
        isSaveExercisePending: false,
        saveExerciseError: action.payload
      }
    case 'CREATE_TRACK_PENDING':
      return {
        ...state,
        isSaveTrackPending: true,
      }
    case 'CREATE_TRACK_FULFILLED':
      return {
        ...state,
        isSaveTrackPending: false,
        tracks: [
          ...state.tracks,
          action.payload.data
        ]
      }
    case 'CREATE_UNIT_PENDING':
      return {
        ...state,
        isSaveUnitPending: true,
      }
    case 'CREATE_UNIT_FULFILLED':
      const createdUnit = action.payload.data
      const updatedTracksWithNewUnit = state.tracks.reduce((acc, tr) => {
        // Identify a track by the update unit's track id
        if (tr.id === createdUnit.track) {
          // Update the track's units list
          tr.track_units.push(createdUnit)
          // ... and put it to the new list of tracks
          acc.push(tr)
        } else {
          // Put non-affected tracks intact
          acc.push(tr)
        }
        return acc
      }, [])
      return {
        ...state,
        isSaveUnitPending: false,
        tracks: updatedTracksWithNewUnit
      }
    case 'CREATE_LESSON_PENDING':
      return {
        ...state,
        isSaveLessonPending: true
      }
    case 'CREATE_LESSON_FULFILLED':
      const createdLesson = action.payload.data
      const updatedTracksWithNewLesson = state.tracks.reduce((tracks, tr, idx) => {
        // Try to update each track's unit's lessons
        const updUnits = tr.track_units.reduce((acc, un) => {
          // Get the lesson's unit by id
          if (un.id === createdLesson.unit) {
            // Add the newly created lesson to the unit's lessons
            un.unit_lessons.push(createdLesson)
            acc.push(un)
          } else {
            acc.push(un)
          }
          return acc
        }, [])
        tr.track_units = updUnits
        tracks.push(tr)
        return tracks
      }, [])
      return {
        ...state,
        isSaveLessonPending: false,
        tracks: updatedTracksWithNewLesson
      }
    case 'CREATE_EXERCISE_PENDING':
      return {
        ...state,
        newlyCreatedExerciseId: null,
        isSaveExercisePending: true
      }
    case 'CREATE_EXERCISE_FULFILLED':
      const newEx = action.payload.data
      return {
        ...state,
        isSaveExercisePending: false,
        newlyCreatedExerciseId: newEx.id,
        exercises: [
          ...state.exercises, newEx
        ]
      }
    case 'RESET_NEWLY_CREATED_EXERCISE_ID':
      return {
        ...state,
        newlyCreatedExerciseId: null
      }
    default:
      return state
  }
}

export default cabinet
