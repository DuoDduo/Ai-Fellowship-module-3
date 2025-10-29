class EnrollmentRequest(BaseModel):
    course_id: int = Field(..., example=1)


@app.post("/enroll")
def enroll_course(input: EnrollmentRequest, user_data=Depends(verify_token)):
    try:
        # Check if user is a student
        if user_data['user_type'] != 'student':
            raise HTTPException(status_code=403, detail="Only students can enroll in courses.")

        # Get user_id from database
        user_query = text("SELECT id FROM users WHERE email = :email")
        user_result = db.execute(user_query, {"email": user_data["email"]}).fetchone()
        if not user_result:
            raise HTTPException(status_code=404, detail="User not found.")
        user_id = user_result.id

        # Check if course exists
        course_query = text("SELECT id FROM courses WHERE id = :course_id")
        course_result = db.execute(course_query, {"course_id": input.course_id}).fetchone()
        if not course_result:
            raise HTTPException(status_code=404, detail="Course not found.")

        # Check if already enrolled
        existing_query = text("SELECT * FROM enrollments WHERE user_id = :user_id AND course_id = :course_id")
        existing = db.execute(existing_query, {"user_id": user_id, "course_id": input.course_id}).fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="Already enrolled in this course.")

        # Enroll user
        enroll_query = text("""
            INSERT INTO enrollments (user_id, course_id)
            VALUES (:user_id, :course_id)
        """)
        db.execute(enroll_query, {"user_id": user_id, "course_id": input.course_id})
        db.commit()

        return {"message": "Enrollment successful", "course_id": input.course_id, "user_id": user_id}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
