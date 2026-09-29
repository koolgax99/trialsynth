"""
Models for the unflattened response from the clinicaltrials.gov REST API.

See https://clinicaltrials.gov/data-api/about-api/study-data-structure
for more details on the structure of the response.
"""
from pydantic import BaseModel, Field


class SecondaryID(BaseModel):

    id_type: str = Field(alias="type")
    secondary_id: str = Field(alias="id")


class IDModule(BaseModel):

    nct_id: str = Field(alias="nctId")
    brief_title: str = Field(alias="briefTitle")
    official_title: str = Field(alias="officialTitle", default=None)
    secondary_ids: list[SecondaryID] = Field(alias="secondaryIds", default=[])


class ConditionsModule(BaseModel):

    conditions: list[str] = Field(default=[])


class DateStruct(BaseModel):

    date: str = Field(default=None)
    date_type: str = Field(alias="type", default=None)


class StatusModule(BaseModel):

    start_date_struct: DateStruct = Field(
        alias="startDateStruct", default=DateStruct()
    )
    primary_completion_date_struct: DateStruct = Field(
        alias="primaryCompletionDateStruct",
        default=DateStruct(),
        description="The date that the final participant was examined or "
                    "received an intervention for the purposes of final "
                    "collection of data for the primary outcome"
    )
    # Also known as "Study Completion Date", see:
    # https://clinicaltrials.gov/policy/protocol-definitions#LastFollowUpDate
    completion_date_struct: DateStruct = Field(
        alias="completionDateStruct",
        default=DateStruct(),
        description="The date the final participant was examined or received "
                    "an intervention for purposes of final collection of data "
                    "for the primary and secondary outcome measures and "
                    "adverse events (for example, last participant’s last "
                    "visit)",
    )
    last_update_submit_date: str = Field(
        alias="lastUpdateSubmitDate", default=None
    )
    overall_status: str = Field(alias="overallStatus", default=None)
    why_stopped: str = Field(alias="whyStopped", default=None)


class DesignMaskingInfo(BaseModel):
    masking: str = Field(alias="masking", default=None)


class DesignInfo(BaseModel):
    purpose: str = Field(alias="primaryPurpose", default=None)
    allocation: str = Field(alias="allocation", default=None)
    masking_info: DesignMaskingInfo = Field(
        alias="maskingInfo", default=DesignMaskingInfo()
    )
    intervention_assignment: str = Field(alias="interventionModel", default=None)
    observation_assignment: str = Field(alias="observationalModel", default=None)


class EnrollmentInfo(BaseModel):

    count: int = Field(default=None)
    # ESTIMATED for the enrollment target, ACTUAL once the trial has run
    enrollment_type: str = Field(alias="type", default=None)


class DesignModule(BaseModel):

    study_type: str = Field(alias="studyType", default=None)
    design_info: DesignInfo = Field(alias="designInfo", default=DesignInfo())
    phases: list[str] = Field(alias="phases", default=[])
    enrollment_info: EnrollmentInfo = Field(
        alias="enrollmentInfo", default=EnrollmentInfo()
    )


class Reference(BaseModel):
    # See: https://clinicaltrials.gov/policy/protocol-definitions#references

    pmid: str = Field(alias="pmid", default=None)  # Reference PMID
    type: str = Field(alias="type", default=None)  # One of BACKGROUND, RESULT, DERIVED
    citation: str = Field(alias="citation", default=None)


class ReferencesModule(BaseModel):

    references: list[Reference] = Field(alias="references", default=[])


class Intervention(BaseModel):

    name: str = Field(default=None)
    intervention_type: str = Field(alias="type")
    description: str = Field(default=None)


class ArmGroup(BaseModel):

    label: str = Field(default=None)
    arm_group_type: str = Field(alias="type", default=None)
    description: str = Field(default=None)
    intervention_names: list[str] = Field(alias="interventionNames", default=[])


class ArmsInterventionsModule(BaseModel):

    arm_groups: list[ArmGroup] = Field(alias="armGroups", default=[])
    arms_interventions: list[Intervention] = Field(alias="interventions", default=[])


class Mesh(BaseModel):

    term: str
    mesh_id: str = Field(alias="id")


class InterventionBrowseModule(BaseModel):

    intervention_meshes: list[Mesh] = Field(alias="meshes", default=[])


class ConditionBrowseModule(BaseModel):

    condition_meshes: list[Mesh] = Field(alias="meshes", default=[])


class Outcome(BaseModel):
    measure: str = Field(alias="measure", default=None)
    time_frame: str = Field(alias="timeframe", default=None)


class OutcomesModule(BaseModel):
    primary_outcome: list[Outcome] = Field(alias="primaryOutcomes", default=[])
    secondary_outcome: list[Outcome] = Field(alias="secondaryOutcomes", default=[])


class EligibilityModule(BaseModel):
    # See: https://clinicaltrials.gov/policy/protocol-definitions#EligibilityCriteria

    eligibility_criteria: str = Field(
        alias="eligibilityCriteria",
        default=None,
        description="Free text listing inclusion and exclusion criteria under "
                    "their own headings. Not a structured field."
    )
    healthy_volunteers: bool = Field(alias="healthyVolunteers", default=None)
    sex: str = Field(default=None)
    minimum_age: str = Field(alias="minimumAge", default=None)
    maximum_age: str = Field(alias="maximumAge", default=None)
    std_ages: list[str] = Field(alias="stdAges", default=[])


class GeoPoint(BaseModel):

    lat: float = Field(default=None)
    lon: float = Field(default=None)


class Location(BaseModel):

    facility: str = Field(default=None)
    city: str = Field(default=None)
    state: str = Field(default=None)
    zip_code: str = Field(alias="zip", default=None)
    country: str = Field(default=None)
    geo_point: GeoPoint = Field(alias="geoPoint", default=GeoPoint())


class ContactsLocationsModule(BaseModel):

    locations: list[Location] = Field(default=[])


class DescriptionModule(BaseModel):

    brief_summary: str = Field(alias="briefSummary", default=None)
    detailed_description: str = Field(alias="detailedDescription", default=None)


class ProtocolSection(BaseModel):

    id_module: IDModule = Field(alias="identificationModule")
    conditions_module: ConditionsModule = Field(
        alias="conditionsModule", default=ConditionsModule()
    )
    description_module: DescriptionModule = Field(
        alias="descriptionModule", default=DescriptionModule()
    )
    design_module: DesignModule = Field(alias="designModule", default=DesignModule())
    arms_interventions_module: ArmsInterventionsModule = Field(
        alias="armsInterventionsModule", default=ArmsInterventionsModule()
    )
    outcomes_module: OutcomesModule = Field(
        alias="outcomesModule", default=OutcomesModule()
    )
    eligibility_module: EligibilityModule = Field(
        alias="eligibilityModule", default=EligibilityModule()
    )
    contacts_locations_module: ContactsLocationsModule = Field(
        alias="contactsLocationsModule", default=ContactsLocationsModule()
    )
    status_module: StatusModule = Field(
        alias="statusModule", default=StatusModule()
    )
    references_module: ReferencesModule = Field(
        alias="referencesModule", default=ReferencesModule()
    )


class ResultGroup(BaseModel):
    # Referred to by ID from every measurement in the same module
    id: str = Field(default=None)
    title: str = Field(default=None)
    description: str = Field(default=None)


class GroupCount(BaseModel):
    group_id: str = Field(alias="groupId", default=None)
    value: str = Field(default=None)


class Denominator(BaseModel):
    units: str = Field(default=None)
    counts: list[GroupCount] = Field(default=[])


class FlowCount(BaseModel):
    group_id: str = Field(alias="groupId", default=None)
    num_subjects: str = Field(alias="numSubjects", default=None)
    num_units: str = Field(alias="numUnits", default=None)
    comment: str = Field(default=None)


class FlowMilestone(BaseModel):
    type: str = Field(default=None)
    comment: str = Field(default=None)
    achievements: list[FlowCount] = Field(default=[])


class FlowDropWithdraw(BaseModel):
    type: str = Field(default=None)
    comment: str = Field(default=None)
    reasons: list[FlowCount] = Field(default=[])


class FlowPeriod(BaseModel):
    title: str = Field(default=None)
    milestones: list[FlowMilestone] = Field(default=[])
    drop_withdraws: list[FlowDropWithdraw] = Field(alias="dropWithdraws", default=[])


class ParticipantFlowModule(BaseModel):
    # See: https://clinicaltrials.gov/policy/results-definitions#Result_ParticipantFlow

    recruitment_details: str = Field(alias="recruitmentDetails", default=None)
    pre_assignment_details: str = Field(alias="preAssignmentDetails", default=None)
    type_units_analyzed: str = Field(alias="typeUnitsAnalyzed", default=None)
    groups: list[ResultGroup] = Field(default=[])
    periods: list[FlowPeriod] = Field(default=[])


class Measurement(BaseModel):
    group_id: str = Field(alias="groupId", default=None)
    value: str = Field(default=None)
    spread: str = Field(default=None)
    lower_limit: str = Field(alias="lowerLimit", default=None)
    upper_limit: str = Field(alias="upperLimit", default=None)
    comment: str = Field(default=None)


class MeasureCategory(BaseModel):
    title: str = Field(default=None)
    measurements: list[Measurement] = Field(default=[])


class MeasureClass(BaseModel):
    title: str = Field(default=None)
    denoms: list[Denominator] = Field(default=[])
    categories: list[MeasureCategory] = Field(default=[])


class Measure(BaseModel):
    title: str = Field(default=None)
    description: str = Field(default=None)
    population_description: str = Field(alias="populationDescription", default=None)
    param_type: str = Field(alias="paramType", default=None)
    dispersion_type: str = Field(alias="dispersionType", default=None)
    unit_of_measure: str = Field(alias="unitOfMeasure", default=None)
    calculate_pct: bool = Field(alias="calculatePct", default=None)
    denom_units_selected: str = Field(alias="denomUnitsSelected", default=None)
    denoms: list[Denominator] = Field(default=[])
    classes: list[MeasureClass] = Field(default=[])


class BaselineCharacteristicsModule(BaseModel):
    # See: https://clinicaltrials.gov/policy/results-definitions#Result_Baseline

    population_description: str = Field(alias="populationDescription", default=None)
    type_units_analyzed: str = Field(alias="typeUnitsAnalyzed", default=None)
    groups: list[ResultGroup] = Field(default=[])
    denoms: list[Denominator] = Field(default=[])
    measures: list[Measure] = Field(default=[])


class OutcomeAnalysis(BaseModel):
    group_ids: list[str] = Field(alias="groupIds", default=[])
    group_description: str = Field(alias="groupDescription", default=None)
    tested_non_inferiority: bool = Field(alias="testedNonInferiority", default=None)
    non_inferiority_type: str = Field(alias="nonInferiorityType", default=None)
    non_inferiority_comment: str = Field(alias="nonInferiorityComment", default=None)
    p_value: str = Field(alias="pValue", default=None)
    p_value_comment: str = Field(alias="pValueComment", default=None)
    statistical_method: str = Field(alias="statisticalMethod", default=None)
    statistical_comment: str = Field(alias="statisticalComment", default=None)
    param_type: str = Field(alias="paramType", default=None)
    param_value: str = Field(alias="paramValue", default=None)
    dispersion_type: str = Field(alias="dispersionType", default=None)
    dispersion_value: str = Field(alias="dispersionValue", default=None)
    ci_pct_value: str = Field(alias="ciPctValue", default=None)
    ci_num_sides: str = Field(alias="ciNumSides", default=None)
    ci_lower_limit: str = Field(alias="ciLowerLimit", default=None)
    ci_lower_limit_comment: str = Field(alias="ciLowerLimitComment", default=None)
    ci_upper_limit: str = Field(alias="ciUpperLimit", default=None)
    ci_upper_limit_comment: str = Field(alias="ciUpperLimitComment", default=None)
    estimate_comment: str = Field(alias="estimateComment", default=None)
    other_analysis_description: str = Field(
        alias="otherAnalysisDescription", default=None
    )


class OutcomeMeasure(BaseModel):
    type: str = Field(default=None)
    title: str = Field(default=None)
    description: str = Field(default=None)
    population_description: str = Field(alias="populationDescription", default=None)
    reporting_status: str = Field(alias="reportingStatus", default=None)
    anticipated_posting_date: str = Field(
        alias="anticipatedPostingDate", default=None
    )
    param_type: str = Field(alias="paramType", default=None)
    dispersion_type: str = Field(alias="dispersionType", default=None)
    unit_of_measure: str = Field(alias="unitOfMeasure", default=None)
    time_frame: str = Field(alias="timeFrame", default=None)
    type_units_analyzed: str = Field(alias="typeUnitsAnalyzed", default=None)
    denom_units_selected: str = Field(alias="denomUnitsSelected", default=None)
    calculate_pct: bool = Field(alias="calculatePct", default=None)
    groups: list[ResultGroup] = Field(default=[])
    denoms: list[Denominator] = Field(default=[])
    classes: list[MeasureClass] = Field(default=[])
    analyses: list[OutcomeAnalysis] = Field(default=[])


class OutcomeMeasuresModule(BaseModel):
    # See: https://clinicaltrials.gov/policy/results-definitions#Result_Outcome_Measure

    outcome_measures: list[OutcomeMeasure] = Field(
        alias="outcomeMeasures", default=[]
    )


class EventStat(BaseModel):
    group_id: str = Field(alias="groupId", default=None)
    num_affected: int = Field(alias="numAffected", default=None)
    num_at_risk: int = Field(alias="numAtRisk", default=None)
    num_events: int = Field(alias="numEvents", default=None)


class AdverseEvent(BaseModel):
    term: str = Field(default=None)
    organ_system: str = Field(alias="organSystem", default=None)
    source_vocabulary: str = Field(alias="sourceVocabulary", default=None)
    assessment_type: str = Field(alias="assessmentType", default=None)
    notes: str = Field(default=None)
    stats: list[EventStat] = Field(default=[])


class AdverseEventGroup(BaseModel):
    id: str = Field(default=None)
    title: str = Field(default=None)
    description: str = Field(default=None)
    serious_num_affected: int = Field(alias="seriousNumAffected", default=None)
    serious_num_at_risk: int = Field(alias="seriousNumAtRisk", default=None)
    other_num_affected: int = Field(alias="otherNumAffected", default=None)
    other_num_at_risk: int = Field(alias="otherNumAtRisk", default=None)
    deaths_num_affected: int = Field(alias="deathsNumAffected", default=None)
    deaths_num_at_risk: int = Field(alias="deathsNumAtRisk", default=None)


class AdverseEventsModule(BaseModel):
    # See: https://clinicaltrials.gov/policy/results-definitions#Result_AdverseEvents

    frequency_threshold: str = Field(alias="frequencyThreshold", default=None)
    time_frame: str = Field(alias="timeFrame", default=None)
    description: str = Field(default=None)
    all_cause_mortality_comment: str = Field(
        alias="allCauseMortalityComment", default=None
    )
    event_groups: list[AdverseEventGroup] = Field(alias="eventGroups", default=[])
    serious_events: list[AdverseEvent] = Field(alias="seriousEvents", default=[])
    other_events: list[AdverseEvent] = Field(alias="otherEvents", default=[])


class ResultsSection(BaseModel):
    # moreInfoModule is not requested: it carries agreements and a point of
    # contact, not trial data.

    participant_flow_module: ParticipantFlowModule = Field(
        alias="participantFlowModule", default=ParticipantFlowModule()
    )
    baseline_characteristics_module: BaselineCharacteristicsModule = Field(
        alias="baselineCharacteristicsModule",
        default=BaselineCharacteristicsModule(),
    )
    outcome_measures_module: OutcomeMeasuresModule = Field(
        alias="outcomeMeasuresModule", default=OutcomeMeasuresModule()
    )
    adverse_events_module: AdverseEventsModule = Field(
        alias="adverseEventsModule", default=AdverseEventsModule()
    )


class DerivedSection(BaseModel):

    condition_browse_module: ConditionBrowseModule = Field(
        alias="conditionBrowseModule", default=ConditionBrowseModule()
    )
    intervention_browse_module: InterventionBrowseModule = Field(
        alias="interventionBrowseModule", default=InterventionBrowseModule()
    )


class UnflattenedTrial(BaseModel):
    """
    Clinicaltrials.gov trial data from REST API response
    """

    protocol_section: ProtocolSection = Field(alias="protocolSection")
    derived_section: DerivedSection = Field(alias="derivedSection")
    results_section: ResultsSection = Field(
        alias="resultsSection",
        default=None,
        description="Present only when the record carries posted results"
    )
    has_results: bool = Field(
        alias="hasResults",
        default=None,
        description="Whether the record carries a resultsSection"
    )
