USE petclinic;

INSERT IGNORE INTO
    appointments (
        id,
        appointment_date,
        description,
        owner_id,
        pet_id
    )
VALUES (
        1,
        '2025-05-01 10:00:00',
        'Annual checkup for Leo and Max',
        1,
        1
    ),
    (
        2,
        '2025-05-02 14:30:00',
        'Vaccination for Basil',
        2,
        2
    ),
    (
        3,
        '2025-05-03 09:15:00',
        'Check skin rash on Rosy',
        3,
        3
    ),
    (
        4,
        '2025-05-04 16:45:00',
        'Dental cleaning for Jewel',
        3,
        4
    ),
    (
        5,
        '2025-05-05 11:00:00',
        'Follow-up for Iggy',
        4,
        5
    ),
    (
        6,
        '2025-05-06 13:00:00',
        'General consultation for George and Sly',
        5,
        6
    );
