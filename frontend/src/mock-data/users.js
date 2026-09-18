export const mockSeniors = [
    {
        id: 101,
        role: "senior",
        name: "Lakshmi",
        age: 72,
        gender: "Female",
        language: "Telugu",
        location: "Vijayawada",
        address: "Plot 42, Moghalrajpuram, Vijayawada",
        caretaker_id: 201,
        blood_group: "O+",
        conditions: ["Mild Hypertension", "Osteoarthritis"],
        allergies: ["Penicillin"],
        notes: "Uses walking cane for long walks. Keep emergency contact notified.",
        medications: [
            { id: 1, name: "Amlodipine (5mg)", time: "08:00 AM", taken: true },
            { id: 2, name: "Metformin (500mg)", time: "12:30 PM", taken: true },
            { id: 3, name: "Atorvastatin (10mg)", time: "02:00 PM", taken: true },
            { id: 4, name: "Calcium + Vit D3", time: "08:00 PM", taken: false }
        ],
        checkin_completed: true,
        status: "Checked in",
    },
    {
        id: 102,
        role: "senior",
        name: "Ramesh",
        age: 68,
        gender: "Male",
        language: "Telugu",
        location: "Vijayawada",
        address: "B-12, Governorpet, Vijayawada",
        caretaker_id: 201,
        blood_group: "B+",
        conditions: ["Type 2 Diabetes"],
        allergies: ["None known"],
        notes: "Blood glucose monitored daily at 7 AM.",
        medications: [
            { id: 1, name: "Metformin (500mg)", time: "08:00 AM", taken: true },
            { id: 2, name: "Glimepiride (1mg)", time: "08:00 PM", taken: false }
        ],
        checkin_completed: true,
        status: "Stable",
    },
    {
        id: 103,
        role: "senior",
        name: "Savitri",
        age: 75,
        gender: "Female",
        language: "Telugu",
        location: "Vijayawada",
        address: "Flat 304, Suryaraopet, Vijayawada",
        caretaker_id: 201,
        blood_group: "A+",
        conditions: ["Mild Asthma", "Cataract (post-op)"],
        allergies: ["Sulfa drugs"],
        notes: "Inhaler kept on bedside table.",
        medications: [
            { id: 1, name: "Budecort Inhaler", time: "Morning & Night", taken: true }
        ],
        checkin_completed: true,
        status: "Stable",
    },
    {
        id: 104,
        role: "senior",
        name: "Krishna Rao",
        age: 80,
        gender: "Male",
        language: "Telugu",
        location: "Vijayawada",
        address: "House 18, Labbipet, Vijayawada",
        caretaker_id: 201,
        blood_group: "AB+",
        conditions: ["Post-Stroke Recovery", "Hypertension"],
        allergies: ["Aspirin"],
        notes: "Physical therapy exercises at 11 AM daily.",
        medications: [
            { id: 1, name: "Telmisartan (40mg)", time: "09:00 AM", taken: true },
            { id: 2, name: "Clopidogrel (75mg)", time: "01:00 PM", taken: true }
        ],
        checkin_completed: true,
        status: "Stable",
    },
    {
        id: 105,
        role: "senior",
        name: "Padma",
        age: 69,
        gender: "Female",
        language: "Telugu",
        location: "Vijayawada",
        address: "7-89, Gunadala, Vijayawada",
        caretaker_id: 201,
        blood_group: "O-",
        conditions: ["Osteopenia"],
        allergies: ["None"],
        notes: "Evening walk around apartment complex.",
        medications: [
            { id: 1, name: "Alendronate (70mg)", time: "Weekly Sunday", taken: true }
        ],
        checkin_completed: true,
        status: "Stable",
    }
];

export const mockUsers = {
    senior: mockSeniors[0],
    caretaker: {
        id: 201,
        role: "caretaker",
        name: "Ravi Kumar",
        status: "Available",
        phone: "+91 98765 43210",
        rating: 4.9,
        assigned_seniors: [101, 102, 103, 104, 105],
    },
    volunteer: {
        id: 301,
        role: "volunteer",
        name: "Priya Sharma",
        phone: "+91 94401 23456",
        distance_km: 2.4,
        eta_minutes: 7,
        available: true,
        skills: ["First Aid", "CPR Certified", "Fall Assistance"],
        rating: 4.95,
        badges: ["Top Responder", "First-Aid Trained"]
    },
    family: {
        id: 401,
        role: "family",
        name: "Anjali",
        phone: "+91 98480 11223",
        relationship: "Daughter",
        connected_senior: 101,
        location: "Vijayawada"
    }
};

export const mockAdditionalCaretakers = [
    {
        id: 202,
        name: "Arun Varma",
        phone: "+91 91234 56789",
        distance_km: 2.1,
        status: "Available",
        skills: ["Mobility Support", "Medical Escort"]
    },
    {
        id: 203,
        name: "Sunita Reddy",
        phone: "+91 92345 67890",
        distance_km: 3.4,
        status: "Available",
        skills: ["Geriatric Nursing", "Vital Signs"]
    }
];
