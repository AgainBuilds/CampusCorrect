
"""
CAMPUSCORRECT ACADEMIC CATALOGUE

Central source of course information.
Add or update course outlines in this file.
The seed system registers courses automatically.
"""

ACADEMIC_CATALOG = {

    # ==================================================
    # MTH 201
    # ==================================================

    "MTH201": {
        "code": "MTH 201",
        "title": "MTH 201",
        "level": 200,
        "semester": "1",
        "programme": "Computer Science & Informatics",

        "outline": [
            {"title": "Real and absolute functions of a real variable"},
            {"title": "Mean Value Theorem"},
            {"title": "Taylor series"},
            {"title": "Real-valued functions of two or three variables"},
            {"title": "Partial derivatives (chain rule)"},
            {"title": "Extrema and Lagrange multipliers"},
            {"title": "Exercises on composition of functions"},
        ],

        "textbooks": [],
        "past_questions": [],
        "contributors": [],
    },

    # ==================================================
    # CSC 201 - PROGRAMMING
    # ==================================================

    "CSC201": {
        "code": "CSC 201",
        "title": "Programming",
        "level": 200,
        "semester": "1",
        "programme": "Computer Science & Informatics",

        "outline": [
            {"title": "Introduction to Computer Programming"},
            {"title": "Datatypes and Variables in C++"},
            {"title": "Input and Output Statements in C++"},
            {"title": "Operators"},
            {"title": "Control Structures"},
            {"title": "Functions"},
            {"title": "Arrays"},
            {"title": "Pointers and Strings"},
            {"title": "Classes and Objects"},
        ],

        "notes": [
            {
                "title": "What is a program?",
                "content": (
                    "A program is a sequence of instructions "
                    "that tells a computer how to perform a task."
                )
            },
            {
                "title": "Why learn programming?",
                "content": (
                    "Programming helps automate tasks, solve problems, "
                    "create software and build computer applications."
                )
            },
        ],

        "textbooks": [],
        "past_questions": [],
        "contributors": [],
    },

    # ==================================================
    # INF 203 - INTRODUCTION TO INFORMATION TECHNOLOGY
    # ==================================================

    "INF203": {
        "code": "INF 203",
        "title": "Introduction to Information Technology",
        "level": 200,
        "semester": "1",
        "programme": "Computer Science & Informatics",

        "outline": [

            {
                "title": "Module 1: Fundamentals of Information Technology",
                "topics": [
                    "Defining Concepts and Scope of IT",
                    "Introduction to Computer Hardware and Software",
                    "Basic functions and components of a computer system",
                    "Types of computer",
                    "Overview of IT systems",
                ]
            },

            {
                "title": "Module 2: Information Technology Systems Models",
                "topics": [
                    "Concepts and Components of an IT system model",
                    "Input, Processing, Output, Storage and feedback",
                    "Data, Information and Knowledge",
                    "Data Versus Information",
                    "Characteristics and quality of good Information",
                ]
            },

            {
                "title": "Module 3: History and Evolution of IT",
                "topics": [
                    "Historical development of computers",
                    "Generations of computers / evolution of computers",
                    "History and development of the Internet",
                    "Milestones in computing and digital communication",
                ]
            },

            {
                "title": "Module 4: Human Computer Interaction (HCI)",
                "topics": [
                    "Introduction to HCI",
                    "User interfaces and Interaction methods",
                    "Usability, accessibility and user experience",
                    "The role of HCI in IT system design",
                ]
            },

            {
                "title": "Module 5: Information Management",
                "topics": [
                    "Concept and principles of Information management",
                    "Data processing and Information system",
                    "Database management fundamentals",
                    "Information storage, retrieval and organization",
                    "Information management in Organizations",
                ]
            },

            {
                "title": "Module 6: Network Technologies",
                "topics": [
                    "Introduction to Computer Network",
                    "Types of Network: LAN, MAN, WAN",
                    "Network components and devices",
                    "Network topologies and Communication protocols",
                    "Wireless and Wired Networking",
                    "Introduction to the internet and Network Services",
                ]
            },

            {
                "title": "Module 7: Platform Technologies",
                "topics": [
                    "Introduction to Computer platforms",
                    "Operating System and their functions",
                    "Desktop, mobile and cloud computing functions",
                    "Visualization and distributed computing",
                    "Hardware and Software platform integration",
                ]
            },
        ],

        "textbooks": [],
        "past_questions": [],
        "contributors": [],
    },

    # ==================================================
    # GET 201 - ENTREPRENEURSHIP
    # ==================================================

    "GET201": {
        "code": "GET 201",
        "title": "Entrepreneurship",
        "level": 200,
        "semester": "1",
        "programme": "Computer Science & Informatics",

        "outline": [

            {
                "title": "Concepts and Nature of Entrepreneurship",
                "topics": [
                    "Meaning and the scope of entrepreneurship",
                    "Entrepreneurship and corporate entrepreneurship",
                    "Differences between entrepreneur, intrapreneur and the manager",
                    "Importance of entrepreneurship in economic development",
                    "Theories of entrepreneurship",
                    "Schumpeter's theory and creative destruction",
                    "Economic, psychological and sociological perspectives",
                    "Risk taking and necessity/opportunity driven entrepreneurship",
                    "Societal and economic relevance of entrepreneurship",
                    "Characteristics or mindset of entrepreneur",
                    "Core traits: opportunity seeking, risk taking, problem solving",
                    "Natural vs nurtured entrepreneurship",
                    "Entrepreneur as innovators and change agents",
                    "Entrepreneur training",
                    "Critical, creative and effective thinking",
                ]
            },

            {
                "title": "Innovation and Change Management",
                "topics": [
                    "Meaning and concepts of innovation",
                    "Dimensions of innovation: product, process, market and organization",
                    "Relationship between knowledge, innovation and change",
                    "Technology and innovation driven enterprise",
                ]
            },

            {
                "title": "Enterprise Formation, Partnership and Networking",
                "topics": [
                    "Basis of business plan",
                    "Forms of business ownership",
                    "Business registration processes",
                    "Partnership formation",
                    "Strategic alliance, networking and Joint Venture",
                ]
            },

            {
                "title": "Contemporary Issues in Entrepreneurship",
                "topics": [
                    "Entrepreneurship knowledge and skills",
                    "Technology, Virtual office and digital workplace",
                    "Intellectual properties: patents, trademarks and copyright",
                ]
            },

            {
                "title": "Entrepreneurship in Nigeria and Introduction to E-commerce",
                "topics": [
                    "Profiles of successful Nigerian entrepreneurs",
                    "Youth and women entrepreneurship initiatives",
                    "Entrepreneurship Support institutions: SMEDAN, BOI, NDE, etc.",
                    "Basic principles of e-commerce",
                ]
            },
        ],

        "textbooks": [],
        "past_questions": [],
        "contributors": [],
    },

    # ==================================================
    # INF 201 - INTRODUCTION TO SOFTWARE ENGINEERING
    # ==================================================

    "INF201": {
        "code": "INF 201",
        "title": "Introduction to Software Engineering",
        "level": 200,
        "semester": "1",
        "programme": "Computer Science & Informatics",

        "definition": (
            "Software engineering is a systematic and disciplined "
            "approach to the specification, design, development, "
            "testing, deployment, maintenance and improvement "
            "of software systems."
        ),

        "outline": [
            {"title": "Introduction to Software Engineering"},
            {"title": "Software Processes and Life Cycle Model"},
            {"title": "Software Requirement and Specification"},
            {"title": "Software Design and Architecture"},
            {"title": "Software Metrics and Quality"},
            {"title": "Software Testing and Validation"},
            {"title": "Software Evolution and Maintenance"},
            {"title": "Software Project Management"},
            {"title": "Software Engineering and Law"},
        ],

        "teacher": "Joy",

        "textbooks": [],
        "past_questions": [],
        "contributors": [],
    },

    # ==================================================
    # CYB 201 - INTRODUCTION TO CYBER SECURITY
    # ==================================================

    "CYB201": {
        "code": "CYB 201",
        "title": "Introduction to Cyber Security",
        "level": 200,
        "semester": "1",
        "programme": "Computer Science & Informatics",

        "outline": [

            {
                "title": "Module 1: Basic Concepts",
                "topics": [
                    "Cyber Security",
                    "Confidentiality, Integrity and Availability",
                    "Authentication",
                    "Access control",
                    "Non-repudiation",
                    "Fault tolerance",
                    "Methodology for implementing Security",
                ]
            },

            {
                "title": "Module 2: Security Policies and Practices",
                "topics": [
                    "Security policies",
                    "Best current practices",
                    "Testing Security",
                    "Incident response",
                ]
            },

            {
                "title": "Module 3: Risk Management",
                "topics": [
                    "Risk management",
                    "Disaster recovery",
                    "Access control",
                ]
            },

            {
                "title": "Module 4: Cryptography and Vulnerabilities",
                "topics": [
                    "Basic cryptography",
                    "Software application Vulnerability",
                ]
            },

            {
                "title": "Module 5: Evolution of Cyber Attacks",
                "topics": [
                    "Evolution of cyber attacks",
                ]
            },

            {
                "title": "Module 6: Security Technologies and Threats",
                "topics": [
                    "Operating system mechanisms",
                    "Intrusion detection systems",
                    "Basic formal model of security",
                    "Cryptography",
                    "Steganography",
                    "Network and distributed system security",
                    "Denial of Service (DoS) and other attack strategies",
                    "Worms and Viruses",
                    "Transfer of funds/Values across networks",
                    "Electronic Voting",
                    "Secure application",
                ]
            },

            {
                "title": "Module 7: Cyber Security Quality and Guidelines",
                "topics": [
                    "Cyber Security quality and guideline",
                    "Government regulation of Information technology",
                    "Main actors of cyber State and Cyber operators",
                ]
            },

            {
                "title": "Module 8: Impact of Cyber Security",
                "topics": [
                    "Impact of cyber security on civil and military",
                    "Privacy",
                    "Business and government applications",
                    "Dimensions of network, protocol, operating systems and associated application",
                ]
            },

            {
                "title": "Module 9: Cyber Security Incidents and Countermeasures",
                "topics": [
                    "Methods and motives of cyber security incidents perpetrated by organizations",
                    "Countermeasures employed by organizations and agencies to prevent and detect incidents",
                ]
            },

            {
                "title": "Module 10: Professional Ethics and Trends",
                "topics": [
                    "Ethical obligation of Security professionals",
                    "Trends and development in cyber Security",
                    "Software Application Vulnerability",
                ]
            },

            {
                "title": "Module 11: Cyber Security and National Security",
                "topics": [
                    "Evolution of cyber security and national security strategies",
                    "Strategies required in the psychology of cyber attacks",
                    "Privacy tools and domestic response",
                ]
            },

            {
                "title": "Module 12: Cybersecurity Strategy and Standards",
                "topics": [
                    "Cybersecurity Strategy involving the face of big risk",
                    "Role of standard",
                ]
            },
        ],

        "textbooks": [],
        "past_questions": [],
        "contributors": [],
    },

    # ==================================================
    # CSC 307 - INTRODUCTION TO WEB TECHNOLOGY
    # ==================================================

    "CSC307": {
        "code": "CSC 307",
        "title": "Introduction to Web Technology",
        "level": 300,
        "semester": "1",
        "programme": "Computer Science & Informatics",

        "outline": [
            {
                "title": "Introduction to the Internet",
                "topics": [
                    "World Wide Web (WWW)",
                    "Web development",
                ]
            },
            {
                "title": "WWW as a Platform",
                "topics": [
                    "WWW as a platform for interactive application/content publishing",
                    "Social Services",
                ]
            },
            {
                "title": "HTTP and HTTPS",
                "topics": [
                    "The role of HTTP/HTTPS in the context of web applications",
                ]
            },
            {
                "title": "Web Browsers and Web Servers",
                "topics": [
                    "Roles and applications of web browsers",
                    "Roles and applications of web servers",
                ]
            },
            {
                "title": "Interacting with Web Applications",
                "topics": [
                    "Interacting with web application through forms",
                    "Style sheets to separate document structure and document forms",
                ]
            },
            {
                "title": "Web Development Tools and Frameworks",
                "topics": [
                    "Web Development tools",
                    "Web Development frameworks",
                ]
            },
        ],

        "textbooks": [],
        "past_questions": [],
        "contributors": [],
    },

}
