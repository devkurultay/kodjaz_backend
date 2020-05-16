export const dataToTree = (data) => {
  return data.map(track => {
    return {
      id: track.id,
      title: track.name,
      subtitle: track.description,
      expanded: false,
      type: track.entity_type,
      // These are needed for saving
      name: track.name,
      description: track.description,
      is_published: track.is_published,
      programming_language: track.programming_language,
      children: getUnits(track.track_units)
    }
  })
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
