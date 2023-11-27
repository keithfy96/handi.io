  OR(
      DATETIME_DIFF({1st Appointment}, NOW(), 'hours') >= 41
    ,
      DATETIME_DIFF({2nd Appointment}, NOW(), 'hours') >= 41
    ,
      DATETIME_DIFF({3rd Appointment}, NOW(), 'hours') >= 41
    ,
      DATETIME_DIFF({4th Appointment}, NOW(), 'hours') >= 41
    
  )


  AC-248-1143