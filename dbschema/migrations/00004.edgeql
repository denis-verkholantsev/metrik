CREATE MIGRATION m1qbzqs7pch2hxm6ibtd7cznag3m3gswhsn7t2fbqa6stcgzsbwika
    ONTO m1avit3shybanhnfbwuzvqlv2f5xxlh26kguvpl3iyr4caslvliqna
{
  ALTER TYPE default::Grade {
      DROP PROPERTY public;
  };
  ALTER TYPE default::SkillTree {
      DROP LINK team;
  };
  ALTER TYPE default::SkillTree {
      CREATE REQUIRED PROPERTY public_grades: std::bool {
          SET default := false;
      };
  };
  ALTER TYPE default::Team {
      DROP PROPERTY description;
      DROP PROPERTY name;
  };
  DROP TYPE default::TeamMember;
  DROP TYPE default::Team;
  DROP SCALAR TYPE default::TeamMemberRole;
};
