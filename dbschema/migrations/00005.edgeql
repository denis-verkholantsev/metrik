CREATE MIGRATION m1lzz3aaix67pkebkcpcc54lfrhjlryeejah3vcbfkvysuhxh2vvvq
    ONTO m1qbzqs7pch2hxm6ibtd7cznag3m3gswhsn7t2fbqa6stcgzsbwika
{
  ALTER TYPE default::Skill {
      CREATE REQUIRED PROPERTY x: std::float64 {
          SET REQUIRED USING (<std::float64>{});
      };
      CREATE REQUIRED PROPERTY y: std::float64 {
          SET REQUIRED USING (<std::float64>{});
      };
  };
};
