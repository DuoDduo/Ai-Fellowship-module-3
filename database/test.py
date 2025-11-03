def enroll_course(input: EnrollmentRequest, user_data=Depends(verify_token)):
    try:
        # Get the user
        user_query = text("SELECT id FROM users WHERE email = :email")
        user_result = db.execute(user_query, {"email": user_data["email"]}).fetchone()

        if not user_result:
            raise HTTPException(status_code=404, detail="User not found.")
        userId = user_result.id

        # Get the course
        if input.course_id:
            course_query = text("SELECT id, title FROM courses WHERE id = :courseId")
            course_result = db.execute(course_query, {"courseId": input.course_id}).fetchone()
        elif input.course_title:
            course_query = text("SELECT id, title FROM courses WHERE title = :title")
            course_result = db.execute(course_query, {"title": input.course_title}).fetchone()
        else:
            raise HTTPException(status_code=400, detail="Please provide either course_id or course_title.")

        if not course_result:
            raise HTTPException(status_code=404, detail="Course not found.")

        courseId = course_result.id
        course_title = course_result.title

        # Check if already enrolled
        existing_query = text("""
            SELECT * FROM enrollments 
            WHERE userId = :userId AND courseId = :courseId
        """)
        existing = db.execute(existing_query, {"userId": userId, "courseId": courseId}).fetchone()

        if existing:
            raise HTTPException(status_code=400, detail=f"Already enrolled in '{course_title}'.")

        # Enroll the user
        enroll_query = text("""
            INSERT INTO enrollments (userId, courseId)
            VALUES (:userId, :courseId)
        """)
        db.execute(enroll_query, {"userId": userId, "courseId": courseId})
        db.commit()

        return {
            "message": f"Enrollment successful in '{course_title}'",
            "userId": userId,
            "courseId": courseId
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
