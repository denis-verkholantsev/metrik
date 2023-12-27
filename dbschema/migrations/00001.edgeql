CREATE MIGRATION m17s457wapiwoq4oqyn5qxa2smtz7bc6l4btoz64qc2mkfnygelg3a
    ONTO initial
{
  CREATE ABSTRACT TYPE default::Auditable {
      CREATE PROPERTY created: std::datetime {
          CREATE REWRITE
              INSERT
              USING (std::datetime_of_statement());
      };
      CREATE PROPERTY modified: std::datetime {
          CREATE REWRITE
              UPDATE
              USING (std::datetime_of_statement());
      };
  };
  CREATE TYPE default::Team EXTENDING default::Auditable {
      CREATE PROPERTY description: std::str;
      CREATE REQUIRED PROPERTY name: std::str;
  };
  CREATE TYPE default::User EXTENDING default::Auditable {
      CREATE REQUIRED PROPERTY email: std::str;
      CREATE INDEX ON (.email);
      CREATE PROPERTY birthdate: cal::local_date;
      CREATE REQUIRED PROPERTY first_name: std::str;
      CREATE REQUIRED PROPERTY last_name: std::str;
      CREATE REQUIRED PROPERTY password: std::str;
  };
  CREATE TYPE default::SkillTree EXTENDING default::Auditable {
      CREATE REQUIRED LINK author: default::User;
      CREATE MULTI LINK likes: default::User;
      CREATE REQUIRED LINK team: default::Team;
      CREATE PROPERTY description: std::str;
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE REQUIRED PROPERTY public: std::bool {
          SET default := false;
      };
  };
  CREATE TYPE default::Skill EXTENDING default::Auditable {
      CREATE REQUIRED LINK author: default::User;
      CREATE REQUIRED LINK tree: default::SkillTree;
      CREATE PROPERTY description: std::str;
      CREATE REQUIRED PROPERTY name: std::str;
  };
  CREATE TYPE default::Grade EXTENDING default::Auditable {
      CREATE REQUIRED LINK author: default::User;
      CREATE REQUIRED LINK skill: default::Skill;
      CREATE REQUIRED PROPERTY public: std::bool {
          SET default := false;
      };
      CREATE REQUIRED PROPERTY value: std::int16;
  };
  CREATE TYPE default::Knowledge EXTENDING default::Auditable {
      CREATE REQUIRED LINK author: default::User;
      CREATE REQUIRED LINK skill: default::Skill;
      CREATE REQUIRED PROPERTY content: std::str;
      CREATE REQUIRED PROPERTY name: std::str;
  };
  CREATE SCALAR TYPE default::TeamMemberRole EXTENDING enum<Guest, Member, Admin>;
  CREATE TYPE default::TeamMember EXTENDING default::Auditable {
      CREATE REQUIRED LINK team: default::Team;
      CREATE REQUIRED LINK user: default::User;
      CREATE PROPERTY role: default::TeamMemberRole {
          SET default := (default::TeamMemberRole.Guest);
      };
  };
};
