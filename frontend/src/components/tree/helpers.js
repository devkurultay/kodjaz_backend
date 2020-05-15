export const dataToTree = (data) => {
  const r = data.map(track => {
    const node = {
      id: track.id,
      title: track.name,
      subtitle: track.description,
      expanded: true,
      children: getUnits(track.track_units)
    }
    return node
  })
  return r
}

const getUnits = (units) => {
  return units.map(unit => {
    return {
      id: unit.id,
      title: unit.name,
      subtitle: unit.description,
      expanded: true,
      children: getLessons(unit.unit_lessons)
    }
  })
}

const getLessons = (lessons) => {
  return lessons.map(lesson => {
    return {
      id: lesson.id,
      title: lesson.name,
      subtitle: lesson.description,
      expanded: true,
      children: getExercises(lesson.lesson_exercises)
    }
  })
}

const getExercises = (exercises) => {
  return exercises.map(exercise => {
    return {
      id: exercise.id,
      title: exercise.name
    }
  })
}
