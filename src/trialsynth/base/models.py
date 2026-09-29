import logging
from datetime import datetime
from typing import Optional, Union, Literal

import indra.statements.agent as agent
from bioregistry import curie_to_str
from indra.ontology.standardize import standardize_name_db_refs

logger = logging.getLogger(__name__)


class SecondaryId:
    """Secondary ID for a trial

    Attributes
    ----------
    ns : str
        The secondary ID's namespace
    id : str
        The ID of the secondary ID
    """

    def __init__(self, ns: str = None, id: str = None):
        self.ns = ns
        self.id = id

    @property
    def curie(self) -> str:
        """Creates a CURIE from the namespace and ID

        Returns
        -------
        str
            The CURIE
        """
        std_name, db_ref = standardize_name_db_refs({self.ns: self.id})
        ns, id = agent.get_grounding(db_ref)
        if ns and id:
            self.ns = ns
            self.id = id

        return curie_to_str(self.ns, self.id)


class DesignInfo:
    """Design information for a trial

    Attributes
    ----------
    purpose : str
        The purpose of the design
    allocation : str
        The allocation of the design
    masking : str
        The masking of the design
    assignment : str
        The assignment of the design
    fallback : Optional[str]
        The fallback design information, if the design information is not in the expected format

    Parameters
    ----------
    purpose : str
        The purpose of the design
    allocation : str
        The allocation of the design
    masking : str
        The masking of the design
    assignment : str
        The assignment of the design
    fallback : Optional[str]
        The fallback design information, if the design information is not in the expected format
    """

    def __init__(
        self,
        purpose=None,
        allocation=None,
        masking=None,
        assignment=None,
        fallback: Optional[str] = None,
    ):
        self.purpose: str = purpose
        self.allocation: str = allocation
        self.masking: str = masking
        self.assignment: str = assignment
        self.fallback: str = fallback


class Outcome:
    """Outcome for a trial

    Attributes
    ----------
    measure : str
        The measure of the outcome
    time_frame : str
        The time frame of the outcome

    Parameters
    ----------
    measure : str
        The measure of the outcome
    time_frame : str
        The time frame of the outcome
    """

    def __init__(self, measure: str = None, time_frame: str = None):
        self.measure = measure
        self.time_frame = time_frame


class Eligibility:
    """Who a trial will and will not enrol

    ``criteria`` is the registry's free-text blob, listing inclusion and
    exclusion criteria under their own headings rather than as separate fields.

    Attributes
    ----------
    criteria : Optional[str]
        Free-text inclusion and exclusion criteria
    sex : Optional[str]
        The sex eligible for the trial, e.g. "FEMALE", "ALL"
    minimum_age : Optional[str]
        The minimum age, as reported, e.g. "18 Years"
    maximum_age : Optional[str]
        The maximum age, as reported, e.g. "85 Years"
    std_ages : list[str]
        Standardized age groups, e.g. ["ADULT", "OLDER_ADULT"]
    healthy_volunteers : Optional[bool]
        Whether the trial accepts healthy volunteers

    Parameters
    ----------
    criteria : Optional[str]
        Free-text inclusion and exclusion criteria
    sex : Optional[str]
        The sex eligible for the trial
    minimum_age : Optional[str]
        The minimum age, as reported
    maximum_age : Optional[str]
        The maximum age, as reported
    std_ages : Optional[list[str]]
        Standardized age groups
    healthy_volunteers : Optional[bool]
        Whether the trial accepts healthy volunteers
    """

    def __init__(
        self,
        criteria: Optional[str] = None,
        sex: Optional[str] = None,
        minimum_age: Optional[str] = None,
        maximum_age: Optional[str] = None,
        std_ages: Optional[list[str]] = None,
        healthy_volunteers: Optional[bool] = None,
    ):
        self.criteria = criteria
        self.sex = sex
        self.minimum_age = minimum_age
        self.maximum_age = maximum_age
        self.std_ages: list[str] = std_ages or []
        self.healthy_volunteers = healthy_volunteers


class Location:
    """A site where a trial is or was run

    Attributes
    ----------
    facility : Optional[str]
        The name of the facility
    city : Optional[str]
        The city the facility is in
    state : Optional[str]
        The state or region the facility is in
    zip_code : Optional[str]
        The postal code of the facility
    country : Optional[str]
        The country the facility is in
    latitude : Optional[float]
        The latitude of the facility, as geocoded by the registry
    longitude : Optional[float]
        The longitude of the facility, as geocoded by the registry

    Parameters
    ----------
    facility : Optional[str]
        The name of the facility
    city : Optional[str]
        The city the facility is in
    state : Optional[str]
        The state or region the facility is in
    zip_code : Optional[str]
        The postal code of the facility
    country : Optional[str]
        The country the facility is in
    latitude : Optional[float]
        The latitude of the facility
    longitude : Optional[float]
        The longitude of the facility
    """

    def __init__(
        self,
        facility: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zip_code: Optional[str] = None,
        country: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
    ):
        self.facility = facility
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.latitude = latitude
        self.longitude = longitude


class ArmGroup:
    """A planned participant group in a trial's protocol

    Attributes
    ----------
    label : Optional[str]
        The group's name, as written in the protocol
    type : Optional[str]
        The group's role, e.g. "experimental", "active_comparator"
    description : Optional[str]
        Free-text description of what the group receives
    intervention_names : list[str]
        The interventions assigned to the group, as the registry names them,
        e.g. "Drug: Rucaparib"

    Parameters
    ----------
    label : Optional[str]
        The group's name, as written in the protocol
    type : Optional[str]
        The group's role
    description : Optional[str]
        Free-text description of what the group receives
    intervention_names : Optional[list[str]]
        The interventions assigned to the group
    """

    def __init__(
        self,
        label: Optional[str] = None,
        type: Optional[str] = None,
        description: Optional[str] = None,
        intervention_names: Optional[list[str]] = None,
    ):
        self.label = label
        self.type = type
        self.description = description
        self.intervention_names: list[str] = intervention_names or []


# types of all nodes should be standardized to a class holding enumerations in the future.


class Node:
    """Node for a trial or bioentity

    Attributes
    ----------
    ns : str
        The namespace of the node
    ns_id : str
        The ID of the node
    labels : list[str]
        The labels of the node (default: []).
    source : Optional[str]
        The source registry of the node

    Parameters
    ----------
    ns : str
        The namespace of the node (default: None).
    ns_id : str
        The ID of the node (default: None).
    """

    def __init__(
        self,
        source: str,
        ns: str = None,
        ns_id: str = None,
    ):
        self.ns: str = ns
        self.ns_id: str = ns_id
        self.labels: list[str] = []
        self.source: str = source

    @property
    def curie(self) -> str:
        if not self.ns or not self.ns_id:
            logger.warning(
                f"{self} does not have a namespace or ID to produce a CURIE with."
            )
            return ""
        return curie_to_str(self.ns.lower(), self.ns_id)

    @curie.setter
    def curie(self, curie: str):
        self.ns, self.ns_id = curie.split(":")


class BioEntity(Node):
    """Holds information about a biological entity

    Attributes
    ----------
    ns: str
        The namespace of the bioentity
    id: str
        The ID of the bioentity
    source: Optional[str]
        The source registry of the bioentity
    text: str
        The free-text of the bioentity
    description: Optional[str]
        The description of the bioentity
    labels: list[str]
        The labels of the bioentity
    grounded_term: Optional[str]
        The entry-term for the grounded bioentity from the given namespace
    origin: Optional[str]
        The trial CURIE that the bioentity is associated with

    Parameters
    ----------
    text: str
        The text term of the bioentity from the given namespace
    labels: list[str]
        The labels of the bioentity
    origin: str
        The trial CURIE that the bioentity is associated with
    source: Optional[str]
        The source registry of the bioentity.
    ns: Optional[str]
        The namespace of the bioentity (default: None).
    id: Optional[str]
        The ID of the bioentity (default: None).
    """

    def __init__(
        self,
        text: str,
        labels: list[str],
        origin: str,
        source: str,
        grounding_source: Optional[Literal["gilda", "mesh"]] = None,
        description: Optional[str] = None,
        ns: Optional[str] = None,
        id: Optional[str] = None,
        grounded_term: Optional[str] = None,
    ):
        super().__init__(ns=ns, ns_id=id, source=source)
        self.labels = labels
        self.text: str = text
        self.description: str = description
        self.origin: str = origin
        self.grounded_term: str = grounded_term
        self.grounding_source: str = grounding_source


class Condition(BioEntity):
    """Represents a condition in a clinical trial

    Parameters
    ----------
    text: str
        The text term of the bioentity from the given namespace
    description: Optional[str]
        The description of the bioentity (default: None).
    labels: list[str]
        The labels of the bioentity
    origin: str
        The trial CURIE that the bioentity is associated with
    source: Optional[str]
        The source registry of the bioentity.
    ns: Optional[str]
        The namespace of the bioentity (default: None).
    id: Optional[str]
        The ID of the bioentity (default: None).
    """

    def __init__(
        self,
        text: str,
        origin: str,
        source: str,
        grounding_source: Optional[Literal["gilda", "mesh"]] = None,
        description: Optional[str] = None,
        labels: Optional[list[str]] = None,
        ns: Optional[str] = None,
        id: Optional[str] = None,
    ):
        super().__init__(
            text=text,
            labels=['condition'],
            origin=origin,
            source=source,
            grounding_source=grounding_source,
            ns=ns,
            id=id,
            description=description,
        )
        if labels:
            self.labels.extend(labels)


class Intervention(BioEntity):
    """
    Represents an intervention in a clinical trial.

    Attributes
    ----------
    text : str
        The text term of the intervention.
    origin : str
        The trial CURIE that the intervention is associated with.
    source : str
        The source registry of the intervention.
    description : Optional[str]
        The description of the intervention (default: None).
    labels : list[str], optional
        Additional labels for the intervention (default: ['intervention']).
    ns : str, optional
        The namespace of the intervention (default: None).
    id : str, optional
        The ID of the intervention (default: None).

    Parameters
    ----------
    text : str
        The text term of the intervention.
    origin : str
        The trial CURIE that the intervention is associated with.
    source : str
        The source registry of the intervention.
    labels : list[str], optional
        Additional labels for the intervention (default: None).
    ns : str, optional
        The namespace of the intervention (default: None).
    id : str, optional
        The ID of the intervention (default: None).
    """
    def __init__(
        self,
        text: str,
        origin: str,
        source: str,
        grounding_source: Optional[Literal["gilda", "mesh"]] = None,
        description: Optional[str] = None,
        labels: Optional[list[str]] = None,
        ns: Optional[str] = None,
        id: Optional[str] = None,
    ):
        super().__init__(
            text=text,
            description=description,
            labels=['intervention'],
            origin=origin,
            grounding_source=grounding_source,
            source=source,
            ns=ns,
            id=id
        )
        if labels:
            self.labels.extend(labels)


# Results reporting. These mirror the registry's own table structure -- groups
# down one axis, measures down the other -- because that is what the data is:
# every value is only meaningful next to the group it was measured in.


class ResultGroup:
    """A participant group a results table reports on

    The registry gives each group an ID (``FG000``, ``BG000``, ``OG000``,
    ``EG000``) that the measurements refer back to. IDs are unique within a
    module, not across them.

    Attributes
    ----------
    id : Optional[str]
        The group's ID within its module, e.g. "OG000"
    title : Optional[str]
        The group's name, as the results report it
    description : Optional[str]
        Free-text description of what the group received

    Parameters
    ----------
    id : Optional[str]
        The group's ID within its module, e.g. "OG000"
    title : Optional[str]
        The group's name, as the results report it
    description : Optional[str]
        Free-text description of what the group received
    """

    def __init__(
        self,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ):
        self.id = id
        self.title = title
        self.description = description


class GroupCount:
    """A per-group participant count, used as a denominator

    Attributes
    ----------
    group_id : Optional[str]
        The ID of the group counted
    value : Optional[str]
        The count, as reported

    Parameters
    ----------
    group_id : Optional[str]
        The ID of the group counted
    value : Optional[str]
        The count, as reported
    """

    def __init__(
        self,
        group_id: Optional[str] = None,
        value: Optional[str] = None,
    ):
        self.group_id = group_id
        self.value = value


class Denominator:
    """The population a set of measurements is reported against

    Attributes
    ----------
    units : Optional[str]
        What is being counted, e.g. "Participants"
    counts : list[GroupCount]
        The count for each group

    Parameters
    ----------
    units : Optional[str]
        What is being counted, e.g. "Participants"
    counts : Optional[list[GroupCount]]
        The count for each group
    """

    def __init__(
        self,
        units: Optional[str] = None,
        counts: Optional[list[GroupCount]] = None,
    ):
        self.units = units
        self.counts: list[GroupCount] = counts or []


class FlowCount:
    """Participants reaching a milestone, or dropping out for one reason

    Attributes
    ----------
    group_id : Optional[str]
        The ID of the group counted
    num_subjects : Optional[str]
        The number of participants, as reported
    num_units : Optional[str]
        The number of units, when units are not participants
    comment : Optional[str]
        Free-text note on the count

    Parameters
    ----------
    group_id : Optional[str]
        The ID of the group counted
    num_subjects : Optional[str]
        The number of participants, as reported
    num_units : Optional[str]
        The number of units, when units are not participants
    comment : Optional[str]
        Free-text note on the count
    """

    def __init__(
        self,
        group_id: Optional[str] = None,
        num_subjects: Optional[str] = None,
        num_units: Optional[str] = None,
        comment: Optional[str] = None,
    ):
        self.group_id = group_id
        self.num_subjects = num_subjects
        self.num_units = num_units
        self.comment = comment


class FlowMilestone:
    """A point participants pass through, e.g. "STARTED", "COMPLETED"

    Attributes
    ----------
    type : Optional[str]
        The milestone, as the registry names it
    comment : Optional[str]
        Free-text note on the milestone
    achievements : list[FlowCount]
        How many participants reached it, per group

    Parameters
    ----------
    type : Optional[str]
        The milestone, as the registry names it
    comment : Optional[str]
        Free-text note on the milestone
    achievements : Optional[list[FlowCount]]
        How many participants reached it, per group
    """

    def __init__(
        self,
        type: Optional[str] = None,
        comment: Optional[str] = None,
        achievements: Optional[list[FlowCount]] = None,
    ):
        self.type = type
        self.comment = comment
        self.achievements: list[FlowCount] = achievements or []


class FlowDropWithdraw:
    """One reason participants left, counted per group

    Attributes
    ----------
    type : Optional[str]
        The reason, e.g. "Withdrawal by Subject"
    comment : Optional[str]
        Free-text note on the reason
    reasons : list[FlowCount]
        How many participants left for it, per group

    Parameters
    ----------
    type : Optional[str]
        The reason, e.g. "Withdrawal by Subject"
    comment : Optional[str]
        Free-text note on the reason
    reasons : Optional[list[FlowCount]]
        How many participants left for it, per group
    """

    def __init__(
        self,
        type: Optional[str] = None,
        comment: Optional[str] = None,
        reasons: Optional[list[FlowCount]] = None,
    ):
        self.type = type
        self.comment = comment
        self.reasons: list[FlowCount] = reasons or []


class FlowPeriod:
    """A stage of the trial that participants flow through

    Attributes
    ----------
    title : Optional[str]
        The stage's name, e.g. "Open-label run-in Period"
    milestones : list[FlowMilestone]
        The points participants passed through
    drop_withdraws : list[FlowDropWithdraw]
        Why participants left during the stage

    Parameters
    ----------
    title : Optional[str]
        The stage's name, e.g. "Open-label run-in Period"
    milestones : Optional[list[FlowMilestone]]
        The points participants passed through
    drop_withdraws : Optional[list[FlowDropWithdraw]]
        Why participants left during the stage
    """

    def __init__(
        self,
        title: Optional[str] = None,
        milestones: Optional[list[FlowMilestone]] = None,
        drop_withdraws: Optional[list[FlowDropWithdraw]] = None,
    ):
        self.title = title
        self.milestones: list[FlowMilestone] = milestones or []
        self.drop_withdraws: list[FlowDropWithdraw] = drop_withdraws or []


class ParticipantFlow:
    """How many participants started, continued and left, per group

    Attributes
    ----------
    recruitment_details : Optional[str]
        Free-text account of how participants were recruited
    pre_assignment_details : Optional[str]
        What happened between recruitment and assignment
    type_units_analyzed : Optional[str]
        The unit counted, when it is not participants
    groups : list[ResultGroup]
        The groups the flow is reported for
    periods : list[FlowPeriod]
        The stages participants flowed through

    Parameters
    ----------
    recruitment_details : Optional[str]
        Free-text account of how participants were recruited
    pre_assignment_details : Optional[str]
        What happened between recruitment and assignment
    type_units_analyzed : Optional[str]
        The unit counted, when it is not participants
    groups : Optional[list[ResultGroup]]
        The groups the flow is reported for
    periods : Optional[list[FlowPeriod]]
        The stages participants flowed through
    """

    def __init__(
        self,
        recruitment_details: Optional[str] = None,
        pre_assignment_details: Optional[str] = None,
        type_units_analyzed: Optional[str] = None,
        groups: Optional[list[ResultGroup]] = None,
        periods: Optional[list[FlowPeriod]] = None,
    ):
        self.recruitment_details = recruitment_details
        self.pre_assignment_details = pre_assignment_details
        self.type_units_analyzed = type_units_analyzed
        self.groups: list[ResultGroup] = groups or []
        self.periods: list[FlowPeriod] = periods or []


class Measurement:
    """One reported value, for one group, in one category

    Attributes
    ----------
    group_id : Optional[str]
        The ID of the group measured
    value : Optional[str]
        The value, as reported
    spread : Optional[str]
        The dispersion around the value, e.g. a standard deviation
    lower_limit : Optional[str]
        The lower end of the reported interval
    upper_limit : Optional[str]
        The upper end of the reported interval
    comment : Optional[str]
        Free-text note on the measurement

    Parameters
    ----------
    group_id : Optional[str]
        The ID of the group measured
    value : Optional[str]
        The value, as reported
    spread : Optional[str]
        The dispersion around the value, e.g. a standard deviation
    lower_limit : Optional[str]
        The lower end of the reported interval
    upper_limit : Optional[str]
        The upper end of the reported interval
    comment : Optional[str]
        Free-text note on the measurement
    """

    def __init__(
        self,
        group_id: Optional[str] = None,
        value: Optional[str] = None,
        spread: Optional[str] = None,
        lower_limit: Optional[str] = None,
        upper_limit: Optional[str] = None,
        comment: Optional[str] = None,
    ):
        self.group_id = group_id
        self.value = value
        self.spread = spread
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.comment = comment


class MeasureCategory:
    """One row of a measure's table, e.g. the "Female" row of a sex measure

    Attributes
    ----------
    title : Optional[str]
        The row's label
    measurements : list[Measurement]
        The value for each group

    Parameters
    ----------
    title : Optional[str]
        The row's label
    measurements : Optional[list[Measurement]]
        The value for each group
    """

    def __init__(
        self,
        title: Optional[str] = None,
        measurements: Optional[list[Measurement]] = None,
    ):
        self.title = title
        self.measurements: list[Measurement] = measurements or []


class MeasureClass:
    """A sub-table of a measure, used when it is reported per stratum

    Attributes
    ----------
    title : Optional[str]
        The stratum's label
    denominators : list[Denominator]
        The population this sub-table is reported against
    categories : list[MeasureCategory]
        The rows of the sub-table

    Parameters
    ----------
    title : Optional[str]
        The stratum's label
    denominators : Optional[list[Denominator]]
        The population this sub-table is reported against
    categories : Optional[list[MeasureCategory]]
        The rows of the sub-table
    """

    def __init__(
        self,
        title: Optional[str] = None,
        denominators: Optional[list[Denominator]] = None,
        categories: Optional[list[MeasureCategory]] = None,
    ):
        self.title = title
        self.denominators: list[Denominator] = denominators or []
        self.categories: list[MeasureCategory] = categories or []


class Measure:
    """A baseline characteristic, reported per group

    ``param_type`` names what the values are (``MEAN``,
    ``COUNT_OF_PARTICIPANTS`` and so on) and ``dispersion_type`` what
    ``Measurement.spread`` holds.

    Attributes
    ----------
    title : Optional[str]
        The characteristic measured, e.g. "Age, Continuous"
    description : Optional[str]
        Free-text description of the measure
    population_description : Optional[str]
        Who the measure was taken over
    param_type : Optional[str]
        What the values are
    dispersion_type : Optional[str]
        What the spread of each value is
    unit_of_measure : Optional[str]
        The unit the values are in, e.g. "year"
    calculate_pct : Optional[bool]
        Whether the values are percentages
    denom_units_selected : Optional[str]
        The unit the measure's denominators count
    denominators : list[Denominator]
        The population the measure is reported against
    classes : list[MeasureClass]
        The measure's table, one entry per stratum

    Parameters
    ----------
    title : Optional[str]
        The characteristic measured, e.g. "Age, Continuous"
    description : Optional[str]
        Free-text description of the measure
    population_description : Optional[str]
        Who the measure was taken over
    param_type : Optional[str]
        What the values are
    dispersion_type : Optional[str]
        What the spread of each value is
    unit_of_measure : Optional[str]
        The unit the values are in, e.g. "year"
    calculate_pct : Optional[bool]
        Whether the values are percentages
    denom_units_selected : Optional[str]
        The unit the measure's denominators count
    denominators : Optional[list[Denominator]]
        The population the measure is reported against
    classes : Optional[list[MeasureClass]]
        The measure's table, one entry per stratum
    """

    def __init__(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        population_description: Optional[str] = None,
        param_type: Optional[str] = None,
        dispersion_type: Optional[str] = None,
        unit_of_measure: Optional[str] = None,
        calculate_pct: Optional[bool] = None,
        denom_units_selected: Optional[str] = None,
        denominators: Optional[list[Denominator]] = None,
        classes: Optional[list[MeasureClass]] = None,
    ):
        self.title = title
        self.description = description
        self.population_description = population_description
        self.param_type = param_type
        self.dispersion_type = dispersion_type
        self.unit_of_measure = unit_of_measure
        self.calculate_pct = calculate_pct
        self.denom_units_selected = denom_units_selected
        self.denominators: list[Denominator] = denominators or []
        self.classes: list[MeasureClass] = classes or []


class BaselineCharacteristics:
    """Who was actually enrolled: demographics and baseline measures

    Attributes
    ----------
    population_description : Optional[str]
        Who the baseline is reported over
    type_units_analyzed : Optional[str]
        The unit measured, when it is not participants
    groups : list[ResultGroup]
        The groups the baseline is reported for
    denominators : list[Denominator]
        The population the measures are reported against
    measures : list[Measure]
        The characteristics measured

    Parameters
    ----------
    population_description : Optional[str]
        Who the baseline is reported over
    type_units_analyzed : Optional[str]
        The unit measured, when it is not participants
    groups : Optional[list[ResultGroup]]
        The groups the baseline is reported for
    denominators : Optional[list[Denominator]]
        The population the measures are reported against
    measures : Optional[list[Measure]]
        The characteristics measured
    """

    def __init__(
        self,
        population_description: Optional[str] = None,
        type_units_analyzed: Optional[str] = None,
        groups: Optional[list[ResultGroup]] = None,
        denominators: Optional[list[Denominator]] = None,
        measures: Optional[list[Measure]] = None,
    ):
        self.population_description = population_description
        self.type_units_analyzed = type_units_analyzed
        self.groups: list[ResultGroup] = groups or []
        self.denominators: list[Denominator] = denominators or []
        self.measures: list[Measure] = measures or []


class OutcomeAnalysis:
    """A statistical comparison between groups for one outcome measure

    Attributes
    ----------
    group_ids : list[str]
        The IDs of the groups compared
    group_description : Optional[str]
        Free-text description of the comparison
    tested_non_inferiority : Optional[bool]
        Whether the test was one of non-inferiority
    non_inferiority_type : Optional[str]
        The kind of test run
    non_inferiority_comment : Optional[str]
        Free-text note on the test's choice
    p_value : Optional[str]
        The p-value, as reported, e.g. "<0.0001"
    p_value_comment : Optional[str]
        Free-text note on the p-value
    statistical_method : Optional[str]
        The method used, e.g. "ANCOVA"
    statistical_comment : Optional[str]
        Free-text note on the method
    param_type : Optional[str]
        What ``param_value`` is
    param_value : Optional[str]
        The estimate, as reported
    dispersion_type : Optional[str]
        What ``dispersion_value`` is
    dispersion_value : Optional[str]
        The dispersion around the estimate
    ci_pct_value : Optional[str]
        The confidence interval's level, e.g. "95"
    ci_num_sides : Optional[str]
        Whether the interval is one- or two-sided
    ci_lower_limit : Optional[str]
        The interval's lower bound
    ci_lower_limit_comment : Optional[str]
        Free-text note on the lower bound
    ci_upper_limit : Optional[str]
        The interval's upper bound
    ci_upper_limit_comment : Optional[str]
        Free-text note on the upper bound
    estimate_comment : Optional[str]
        Free-text note on the estimate
    other_analysis_description : Optional[str]
        Description of an analysis the fields above do not fit

    Parameters
    ----------
    group_ids : Optional[list[str]]
        The IDs of the groups compared
    group_description : Optional[str]
        Free-text description of the comparison
    tested_non_inferiority : Optional[bool]
        Whether the test was one of non-inferiority
    non_inferiority_type : Optional[str]
        The kind of test run
    non_inferiority_comment : Optional[str]
        Free-text note on the test's choice
    p_value : Optional[str]
        The p-value, as reported, e.g. "<0.0001"
    p_value_comment : Optional[str]
        Free-text note on the p-value
    statistical_method : Optional[str]
        The method used, e.g. "ANCOVA"
    statistical_comment : Optional[str]
        Free-text note on the method
    param_type : Optional[str]
        What ``param_value`` is
    param_value : Optional[str]
        The estimate, as reported
    dispersion_type : Optional[str]
        What ``dispersion_value`` is
    dispersion_value : Optional[str]
        The dispersion around the estimate
    ci_pct_value : Optional[str]
        The confidence interval's level, e.g. "95"
    ci_num_sides : Optional[str]
        Whether the interval is one- or two-sided
    ci_lower_limit : Optional[str]
        The interval's lower bound
    ci_lower_limit_comment : Optional[str]
        Free-text note on the lower bound
    ci_upper_limit : Optional[str]
        The interval's upper bound
    ci_upper_limit_comment : Optional[str]
        Free-text note on the upper bound
    estimate_comment : Optional[str]
        Free-text note on the estimate
    other_analysis_description : Optional[str]
        Description of an analysis the fields above do not fit
    """

    def __init__(
        self,
        group_ids: Optional[list[str]] = None,
        group_description: Optional[str] = None,
        tested_non_inferiority: Optional[bool] = None,
        non_inferiority_type: Optional[str] = None,
        non_inferiority_comment: Optional[str] = None,
        p_value: Optional[str] = None,
        p_value_comment: Optional[str] = None,
        statistical_method: Optional[str] = None,
        statistical_comment: Optional[str] = None,
        param_type: Optional[str] = None,
        param_value: Optional[str] = None,
        dispersion_type: Optional[str] = None,
        dispersion_value: Optional[str] = None,
        ci_pct_value: Optional[str] = None,
        ci_num_sides: Optional[str] = None,
        ci_lower_limit: Optional[str] = None,
        ci_lower_limit_comment: Optional[str] = None,
        ci_upper_limit: Optional[str] = None,
        ci_upper_limit_comment: Optional[str] = None,
        estimate_comment: Optional[str] = None,
        other_analysis_description: Optional[str] = None,
    ):
        self.group_ids: list[str] = group_ids or []
        self.group_description = group_description
        self.tested_non_inferiority = tested_non_inferiority
        self.non_inferiority_type = non_inferiority_type
        self.non_inferiority_comment = non_inferiority_comment
        self.p_value = p_value
        self.p_value_comment = p_value_comment
        self.statistical_method = statistical_method
        self.statistical_comment = statistical_comment
        self.param_type = param_type
        self.param_value = param_value
        self.dispersion_type = dispersion_type
        self.dispersion_value = dispersion_value
        self.ci_pct_value = ci_pct_value
        self.ci_num_sides = ci_num_sides
        self.ci_lower_limit = ci_lower_limit
        self.ci_lower_limit_comment = ci_lower_limit_comment
        self.ci_upper_limit = ci_upper_limit
        self.ci_upper_limit_comment = ci_upper_limit_comment
        self.estimate_comment = estimate_comment
        self.other_analysis_description = other_analysis_description


class OutcomeResult:
    """What a pre-specified outcome measure actually found

    This is the reported counterpart of the planned :class:`Outcome`: same
    measure and time frame, but carrying the values and the analyses.

    Attributes
    ----------
    type : Optional[str]
        Whether the outcome is "primary", "secondary" or "other_pre_specified"
    title : Optional[str]
        The outcome measured
    description : Optional[str]
        Free-text description of the outcome
    population_description : Optional[str]
        Who the outcome was measured over
    reporting_status : Optional[str]
        Whether the results are posted or still pending
    anticipated_posting_date : Optional[str]
        When pending results are due
    param_type : Optional[str]
        What the values are
    dispersion_type : Optional[str]
        What the spread of each value is
    unit_of_measure : Optional[str]
        The unit the values are in, e.g. "mmHg"
    time_frame : Optional[str]
        When the outcome was measured
    type_units_analyzed : Optional[str]
        The unit analyzed, when it is not participants
    denom_units_selected : Optional[str]
        The unit the denominators count
    calculate_pct : Optional[bool]
        Whether the values are percentages
    groups : list[ResultGroup]
        The groups the outcome is reported for
    denominators : list[Denominator]
        The population the values are reported against
    classes : list[MeasureClass]
        The outcome's table, one entry per stratum
    analyses : list[OutcomeAnalysis]
        The statistical comparisons run on the outcome

    Parameters
    ----------
    type : Optional[str]
        Whether the outcome is "primary", "secondary" or "other_pre_specified"
    title : Optional[str]
        The outcome measured
    description : Optional[str]
        Free-text description of the outcome
    population_description : Optional[str]
        Who the outcome was measured over
    reporting_status : Optional[str]
        Whether the results are posted or still pending
    anticipated_posting_date : Optional[str]
        When pending results are due
    param_type : Optional[str]
        What the values are
    dispersion_type : Optional[str]
        What the spread of each value is
    unit_of_measure : Optional[str]
        The unit the values are in, e.g. "mmHg"
    time_frame : Optional[str]
        When the outcome was measured
    type_units_analyzed : Optional[str]
        The unit analyzed, when it is not participants
    denom_units_selected : Optional[str]
        The unit the denominators count
    calculate_pct : Optional[bool]
        Whether the values are percentages
    groups : Optional[list[ResultGroup]]
        The groups the outcome is reported for
    denominators : Optional[list[Denominator]]
        The population the values are reported against
    classes : Optional[list[MeasureClass]]
        The outcome's table, one entry per stratum
    analyses : Optional[list[OutcomeAnalysis]]
        The statistical comparisons run on the outcome
    """

    def __init__(
        self,
        type: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        population_description: Optional[str] = None,
        reporting_status: Optional[str] = None,
        anticipated_posting_date: Optional[str] = None,
        param_type: Optional[str] = None,
        dispersion_type: Optional[str] = None,
        unit_of_measure: Optional[str] = None,
        time_frame: Optional[str] = None,
        type_units_analyzed: Optional[str] = None,
        denom_units_selected: Optional[str] = None,
        calculate_pct: Optional[bool] = None,
        groups: Optional[list[ResultGroup]] = None,
        denominators: Optional[list[Denominator]] = None,
        classes: Optional[list[MeasureClass]] = None,
        analyses: Optional[list[OutcomeAnalysis]] = None,
    ):
        self.type = type
        self.title = title
        self.description = description
        self.population_description = population_description
        self.reporting_status = reporting_status
        self.anticipated_posting_date = anticipated_posting_date
        self.param_type = param_type
        self.dispersion_type = dispersion_type
        self.unit_of_measure = unit_of_measure
        self.time_frame = time_frame
        self.type_units_analyzed = type_units_analyzed
        self.denom_units_selected = denom_units_selected
        self.calculate_pct = calculate_pct
        self.groups: list[ResultGroup] = groups or []
        self.denominators: list[Denominator] = denominators or []
        self.classes: list[MeasureClass] = classes or []
        self.analyses: list[OutcomeAnalysis] = analyses or []


class EventStat:
    """How often one adverse event hit one group

    Attributes
    ----------
    group_id : Optional[str]
        The ID of the group affected
    num_affected : Optional[int]
        How many participants had the event
    num_at_risk : Optional[int]
        How many participants could have had it
    num_events : Optional[int]
        How many times the event occurred

    Parameters
    ----------
    group_id : Optional[str]
        The ID of the group affected
    num_affected : Optional[int]
        How many participants had the event
    num_at_risk : Optional[int]
        How many participants could have had it
    num_events : Optional[int]
        How many times the event occurred
    """

    def __init__(
        self,
        group_id: Optional[str] = None,
        num_affected: Optional[int] = None,
        num_at_risk: Optional[int] = None,
        num_events: Optional[int] = None,
    ):
        self.group_id = group_id
        self.num_affected = num_affected
        self.num_at_risk = num_at_risk
        self.num_events = num_events


class AdverseEvent:
    """One adverse event term, counted per group

    Attributes
    ----------
    term : Optional[str]
        The event, e.g. "Nasopharyngitis"
    organ_system : Optional[str]
        The body system the event belongs to
    source_vocabulary : Optional[str]
        The vocabulary the term comes from, e.g. "MedDRA 14.0"
    assessment_type : Optional[str]
        Whether the event was collected systematically
    notes : Optional[str]
        Free-text note on the event
    stats : list[EventStat]
        The event's counts, per group

    Parameters
    ----------
    term : Optional[str]
        The event, e.g. "Nasopharyngitis"
    organ_system : Optional[str]
        The body system the event belongs to
    source_vocabulary : Optional[str]
        The vocabulary the term comes from, e.g. "MedDRA 14.0"
    assessment_type : Optional[str]
        Whether the event was collected systematically
    notes : Optional[str]
        Free-text note on the event
    stats : Optional[list[EventStat]]
        The event's counts, per group
    """

    def __init__(
        self,
        term: Optional[str] = None,
        organ_system: Optional[str] = None,
        source_vocabulary: Optional[str] = None,
        assessment_type: Optional[str] = None,
        notes: Optional[str] = None,
        stats: Optional[list[EventStat]] = None,
    ):
        self.term = term
        self.organ_system = organ_system
        self.source_vocabulary = source_vocabulary
        self.assessment_type = assessment_type
        self.notes = notes
        self.stats: list[EventStat] = stats or []


class AdverseEventGroup:
    """A group's overall adverse event totals

    Separate from :class:`ResultGroup` because the registry reports the
    serious, other and deaths totals on the group itself.

    Attributes
    ----------
    id : Optional[str]
        The group's ID, e.g. "EG000"
    title : Optional[str]
        The group's name
    description : Optional[str]
        Free-text description of what the group received
    serious_num_affected : Optional[int]
        How many participants had a serious event
    serious_num_at_risk : Optional[int]
        How many participants were at risk of one
    other_num_affected : Optional[int]
        How many participants had a non-serious event
    other_num_at_risk : Optional[int]
        How many participants were at risk of one
    deaths_num_affected : Optional[int]
        How many participants died
    deaths_num_at_risk : Optional[int]
        How many participants were at risk of death

    Parameters
    ----------
    id : Optional[str]
        The group's ID, e.g. "EG000"
    title : Optional[str]
        The group's name
    description : Optional[str]
        Free-text description of what the group received
    serious_num_affected : Optional[int]
        How many participants had a serious event
    serious_num_at_risk : Optional[int]
        How many participants were at risk of one
    other_num_affected : Optional[int]
        How many participants had a non-serious event
    other_num_at_risk : Optional[int]
        How many participants were at risk of one
    deaths_num_affected : Optional[int]
        How many participants died
    deaths_num_at_risk : Optional[int]
        How many participants were at risk of death
    """

    def __init__(
        self,
        id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        serious_num_affected: Optional[int] = None,
        serious_num_at_risk: Optional[int] = None,
        other_num_affected: Optional[int] = None,
        other_num_at_risk: Optional[int] = None,
        deaths_num_affected: Optional[int] = None,
        deaths_num_at_risk: Optional[int] = None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.serious_num_affected = serious_num_affected
        self.serious_num_at_risk = serious_num_at_risk
        self.other_num_affected = other_num_affected
        self.other_num_at_risk = other_num_at_risk
        self.deaths_num_affected = deaths_num_affected
        self.deaths_num_at_risk = deaths_num_at_risk


class AdverseEvents:
    """Serious and other adverse events, per group

    ``other_events`` is filtered by the sponsor at ``frequency_threshold``
    percent, so it is not the full list of everything observed.

    Attributes
    ----------
    frequency_threshold : Optional[str]
        The percentage below which other events were not reported
    time_frame : Optional[str]
        The period events were collected over
    description : Optional[str]
        Free-text description of how events were collected
    all_cause_mortality_comment : Optional[str]
        Free-text note on all-cause mortality
    event_groups : list[AdverseEventGroup]
        The groups events are reported for, with their totals
    serious_events : list[AdverseEvent]
        The serious events reported
    other_events : list[AdverseEvent]
        The non-serious events reported

    Parameters
    ----------
    frequency_threshold : Optional[str]
        The percentage below which other events were not reported
    time_frame : Optional[str]
        The period events were collected over
    description : Optional[str]
        Free-text description of how events were collected
    all_cause_mortality_comment : Optional[str]
        Free-text note on all-cause mortality
    event_groups : Optional[list[AdverseEventGroup]]
        The groups events are reported for, with their totals
    serious_events : Optional[list[AdverseEvent]]
        The serious events reported
    other_events : Optional[list[AdverseEvent]]
        The non-serious events reported
    """

    def __init__(
        self,
        frequency_threshold: Optional[str] = None,
        time_frame: Optional[str] = None,
        description: Optional[str] = None,
        all_cause_mortality_comment: Optional[str] = None,
        event_groups: Optional[list[AdverseEventGroup]] = None,
        serious_events: Optional[list[AdverseEvent]] = None,
        other_events: Optional[list[AdverseEvent]] = None,
    ):
        self.frequency_threshold = frequency_threshold
        self.time_frame = time_frame
        self.description = description
        self.all_cause_mortality_comment = all_cause_mortality_comment
        self.event_groups: list[AdverseEventGroup] = event_groups or []
        self.serious_events: list[AdverseEvent] = serious_events or []
        self.other_events: list[AdverseEvent] = other_events or []


class TrialResults:
    """What a trial reported, as opposed to what its protocol planned

    Only a minority of registry records carry one: roughly 80k of 600k on
    ClinicalTrials.gov. ``Trial.has_results`` says whether to expect it.

    Attributes
    ----------
    participant_flow : Optional[ParticipantFlow]
        How participants moved through the trial
    baseline : Optional[BaselineCharacteristics]
        Who was enrolled
    outcome_results : list[OutcomeResult]
        What the outcome measures found
    adverse_events : Optional[AdverseEvents]
        What harms were reported

    Parameters
    ----------
    participant_flow : Optional[ParticipantFlow]
        How participants moved through the trial
    baseline : Optional[BaselineCharacteristics]
        Who was enrolled
    outcome_results : Optional[list[OutcomeResult]]
        What the outcome measures found
    adverse_events : Optional[AdverseEvents]
        What harms were reported
    """

    def __init__(
        self,
        participant_flow: Optional[ParticipantFlow] = None,
        baseline: Optional[BaselineCharacteristics] = None,
        outcome_results: Optional[list[OutcomeResult]] = None,
        adverse_events: Optional[AdverseEvents] = None,
    ):
        self.participant_flow = participant_flow
        self.baseline = baseline
        self.outcome_results: list[OutcomeResult] = outcome_results or []
        self.adverse_events = adverse_events


class Trial(Node):
    """Holds information about a clinical trial

    Attributes
    ----------
    ns: str
        The namespace of the trial
    id: str
        The ID of the trial
    labels: list[str]
        The labels of the trial (default: ['clinicaltrial']).
    source: Optional[str]
        The source registry of the trial (default: None).
    title: str
        The title of the trial
    official_title: Optional[str]
        The official title of the trial (default: None).
    design: Union[DesignInfo, str]
        The design information of the trial
    conditions: list
        The conditions targeted in the trial
    interventions: list
        The interventions used in the trial
    primary_outcomes: Union[Outcome, str]
        The primary outcome of the trial
    secondary_outcomes: Union[Outcome, str]
        The secondary outcome of the trial
    secondary_ids: Union[list[SecondaryId], list[str]]
        The secondary IDs of the trial
    eligibility: Eligibility
        Who the trial will and will not enrol
    locations: list[Location]
        The sites where the trial is or was run
    arm_groups: list[ArmGroup]
        The participant groups the protocol plans
    enrollment: Optional[int]
        The number of participants, planned or actual
    enrollment_type: Optional[str]
        Whether ``enrollment`` is "estimated" (planned) or "actual" (as run)
    has_results: Optional[bool]
        Whether the registry record carries a results section
    results: Optional[TrialResults]
        What the trial reported, when the record carries a results section

    Parameters
    ----------
    ns : str
        The namespace of the trial
    id : str
        The ID of the trial
    labels : Optional[list[str]]
        The labels of the trial (default: None).
    source : Optional[str]
        The source registry of the trial (default: None).
    """

    def __init__(
        self,
        ns: str,
        id: str,
        labels: Optional[list[str]] = None,
        source: Optional[str] = None,
    ):
        super().__init__(source=source, ns=ns, ns_id=id)
        self.labels: list[str] = ["clinical_trial"]
        self.phases: list[str] = []
        self.start_date: Optional[datetime] = None
        self.start_date_type: Optional[str] = None
        self.completion_date: Optional[datetime] = None
        self.completion_date_type: Optional[str] = None
        self.primary_completion_date: Optional[datetime] = None
        self.primary_completion_date_type: Optional[str] = None
        self.last_update_submit_date: Optional[datetime] = None
        self.overall_status: Optional[str] = None
        self.why_stopped: Optional[str] = None

        if labels:
            self.labels.extend(labels)

        self.title: Optional[str] = None
        self.official_title: Optional[str] = None
        self.brief_summary: Optional[str] = None
        self.detailed_description: Optional[str] = None
        self.design: DesignInfo = DesignInfo()
        self.entities: list[BioEntity] = []
        self.primary_outcomes: list[Union[Outcome, str]] = []
        self.secondary_outcomes: list[Union[Outcome, str]] = []
        self.secondary_ids: list[SecondaryId] = []
        self.references: list[tuple[str, str]] = []
        self.eligibility: Eligibility = Eligibility()
        self.locations: list[Location] = []
        self.arm_groups: list[ArmGroup] = []
        self.enrollment: Optional[int] = None
        self.enrollment_type: Optional[str] = None
        self.has_results: Optional[bool] = None
        self.results: Optional[TrialResults] = None

    @property
    def conditions(self) -> list[Condition]:
        return [entity for entity in self.entities if isinstance(entity, Condition)]

    @property
    def interventions(self) -> list[Intervention]:
        return [entity for entity in self.entities if isinstance(entity, Intervention)]


class Edge:
    """Edge between a trial and a bioentity

    Attributes
    ----------
    trial :
        The trial that has a relation to an entity
    entity :
        The bioentity that is related to the trial.
    rel_type :
        The type of relation.
    grounding_sources :
        The sources of grounding for the bioentity.
    """

    def __init__(
        self,
        trial: Trial,
        entity: BioEntity,
        source: str,
        grounding_sources: list[Literal["gilda", "mesh"]],
    ):
        self.trial = trial
        self.entity = entity
        self.source = source

        self.rel_type = f"has_{type(entity).__name__.lower()}"
        self.grounding_sources: list[Literal["gilda", "mesh"]] = grounding_sources


class PublicationEdge:
    """Edge between a trial and a publication

    Attributes
    ----------
    trial :
        The ID of the trial that has a relation to the publication
    publication :
        The publication that is referenced by the trial
    rel_type :
        The type of relation.
    """

    def __init__(
        self,
        trial: str,
        publication: str,
        source: str,
        ref_type: Optional[str] = None,
    ):
        self.trial = trial
        self.publication = publication
        self.rel_type = "has_publication"
        self.source = source
        self.ref_type = ref_type
