module default {
    abstract type Auditable {
        created: datetime {
            rewrite insert using (datetime_of_statement())
        };
        modified: datetime {
            rewrite update using (datetime_of_statement())
        };
    }

    type Skill extending Auditable {
        required name: str;
        description: str;

        required tree: SkillTree;
        required author: User;
        required x: float64;
        required y: float64;

        multi contains: Skill;
    }

    type Knowledge extending Auditable {
        required name: str;
        required content: str;

        required skill: Skill;
        required author: User;
    }

    type Grade extending Auditable {
        required value: int16;

        required author: User;
        required skill: Skill;
    }

    type SkillTree extending Auditable {
        required name: str;
        required public: bool {
            default := false;
        };
        required public_grades: bool {
            default := false;
        }
        description: str;

        required author: User;
        multi likes: User;
    }

    type ExternalLink extending Auditable {
        required url: str;
        link user: User;
    }

    type User extending Auditable {
        required username: str {
            constraint exclusive;
        }
        required email: str {
            constraint exclusive;
        };
        required first_name: str;
        required last_name: str;
        required password: str;
        birthdate: cal::local_date;
        avatar_url: str;
        description: str;
        location: str;
        occupance: str;

        index on (.email);
        index on (.username);
    }
}
