export const addNewExerciseToTrack = (newExercise, tracks) => {
  const updatedTracks = tracks.reduce((tracksAcc, track) => {
    if (newExercise.track_id === track.id) {
      const updatedTrack = addUpdatedUnitsToTrack(newExercise, track)
      tracksAcc.push(updatedTrack)
    } else {
      tracksAcc.push(track)
    }
    return tracksAcc
  }, [])
  return updatedTracks
}

const addUpdatedUnitsToTrack = (newExercise, track) => {
  const updatedUnits = track.track_units.reduce((unitsAcc, unit) => {
    if (newExercise.unit_id === unit.id) {
      const updatedLessons = addExerciseToLessons(newExercise, unit.unit_lessons)
      unit.unit_lessons = updatedLessons
    }
    unitsAcc.push(unit)
    return unitsAcc
  }, [])
  track.track_units = updatedUnits
  return track
}

const addExerciseToLessons = (newExercise, lessons) => {
  const updatedLessons = lessons.reduce((lessonsAcc, lesson) => {
    if (newExercise.lesson === lesson.id) {
      lesson.lesson_exercises.push(newExercise)
    }
    lessonsAcc.push(lesson)
  return lessonsAcc
  }, [])
  return updatedLessons
}
