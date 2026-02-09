SELECT *
FROM `still-smithy-442121-n3.athelete_shoes.v_athletes_scored`
WHERE has_signature_shoe IN ('N')
ORDER BY endorsement_score DESC;
