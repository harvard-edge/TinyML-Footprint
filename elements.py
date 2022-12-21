from typing import Optional
from dataclasses import dataclass
import json
from functools import partial

import plotly
import plotly.express as px
import pandas as pd

import yaml

from js import document, componentHandler, plotly_render
from pyodide.ffi.wrappers import add_event_listener
from pyodide.code import run_js


@dataclass
class BlockOption:
    desc: str
    footprint: float
    act_desc: Optional[str] = None


def render_block_option(o):
    supporting_el_html = document.createElement("span")
    desc_el = document.createElement("span")
    desc_el.appendChild(document.createTextNode(o.desc))
    br_el = document.createElement("br")
    if o.desc == "Custom":
        footnote_desc = document.createTextNode("Enter value")
    elif o.act_desc is not None:
        footnote_desc = document.createTextNode(f"{o.act_desc}")
    else:
        footnote_desc = document.createTextNode(f"{o.footprint:.2f} kg CO2e")
    footprint_el = document.createElement("span")
    footprint_el.className = "footprint"
    footprint_el.appendChild(footnote_desc)

    for e in [desc_el, br_el, footprint_el]:
        supporting_el_html.appendChild(e)
    return supporting_el_html


def button(button_text, cb):
    e = document.createElement("button")
    e.className = "mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent"
    e.appendChild(document.createTextNode(button_text))
    componentHandler.upgradeElement(e)
    # add_event_listener(e, "click", "Pyscript.globals.get('f')();")
    # e.setAttribute("onclick", evt_handler)

    # e.setAttribute("onclick", "Pyscript.globals.get('f')();")
    # e.setAttribute("onclick", "Pyscript.globals.get('f')();")
    add_event_listener(e, "click", cb)
    return e


def make_cols(row_elems):
    """
    Args:
        row_elems: list[tuple[Element, int]]
    """
    container = document.createElement("div")
    container.className = "container"
    re = document.createElement("div")
    re.className = "row"
    container.appendChild(re)
    for e, w in row_elems:
        ce = document.createElement("div")
        ce.className = f"col-{w}"
        ce.appendChild(e)
        re.appendChild(ce)
    return container


def set_attributes(e, **kwargs):
    for k, v in kwargs.items():
        e.setAttribute(k, v)


def numeric_input_el(state, cb):
    #<form action="#">
    #  <div class="mdl-textfield mdl-js-textfield">
    #    <input class="mdl-textfield__input" type="text" pattern="-?[0-9]*(\.[0-9]+)?" id="sample2">
    #    <label class="mdl-textfield__label" for="sample2">Number...</label>
    #    <span class="mdl-textfield__error">Input is not a number!</span>
    #  </div>
    #</form>
    textfield_el = document.createElement("div")
    textfield_el.className = "mdl-textfield mdl-js-textfield"
    input_el = document.createElement("input")
    input_el.className = "mdl-textfield__input"
    input_el.setAttribute("type", "text")
    input_el.setAttribute("pattern", "-?[0-9]*(\.[0-9]+)?")
    input_id = f"input-{state['docid']}"
    input_el.setAttribute("id", input_id)

    custom_option = state["options"][-1]
    assert custom_option.desc == "Custom"
    if custom_option.footprint > 0:
        input_el.setAttribute("value", str(custom_option.footprint))
    textfield_el.appendChild(input_el)
    label_el = document.createElement("label")
    label_el.className = "mdl-textfield__label"
    label_el.setAttribute("for", input_id)
    placeholder = f"Custom {state['heading']} kg CO2e"
    label_el.appendChild(document.createTextNode(placeholder))
    textfield_el.appendChild(label_el)
    error_el = document.createElement("span")
    error_el.className = "mdl-textfield__error"
    error_el.appendChild(document.createTextNode("Input is not a number!"))
    textfield_el.appendChild(error_el)
    componentHandler.upgradeElement(textfield_el)

    def update(_):
        num_options = len(state["options"])
        custom_option = state["options"][-1]
        assert custom_option.desc == "Custom"
        try:
            custom_option.footprint = float(input_el.value)
            state["selected"] = num_options - 1
            cb(None)
        except ValueError:
            custom_option.footprint = 0

    add_event_listener(input_el, "change", update)
    return textfield_el


def checkbox(state, cb):
    # <label class="mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect" for="checkbox-1">
    #   <input type="checkbox" id="checkbox-1" class="mdl-checkbox__input" checked>
    #   <span class="mdl-checkbox__label">Checkbox</span>
    # </label>
    label_el = document.createElement("label")
    label_el.className = "mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect"
    label_el.setAttribute("for", state["docid"])
    input_el = document.createElement("input")
    input_el.setAttribute("type", "checkbox")
    input_el.className = "mdl-checkbox__input"
    input_el.setAttribute("id", state["docid"])
    if state["enabled"]:
        input_el.setAttribute("checked", "checked")
    label_el.appendChild(input_el)
    span_el = document.createElement("span")
    span_el.className = "mdl-checkbox__label"
    span_el.appendChild(document.createTextNode(state["heading"]))
    label_el.appendChild(span_el)
    componentHandler.upgradeElement(label_el)

    def toggle(_):
        state["enabled"] = not state["enabled"]
        cb(None)

    add_event_listener(input_el, "change", toggle)
    return label_el


def block_option(ix, state, cb):
    card_el = document.createElement("div")
    if ix == state["selected"]:
        if state["enabled"]:
            shadow = "mdl-card-active mdl-shadow--4dp"
        else:
            shadow = "mdl-card-ignore mdl-shadow--4dp"
    else:
        shadow = "mdl-card-inactive mdl-shadow--2dp"
    card_el.className = f"mdl-card mdl-card-mmaz {shadow}"
    supporting_el = document.createElement("div")
    supporting_el.className = "mdl-card__supporting-text mdl-card__supporting-text-mmaz"
    supporting_el.appendChild(render_block_option(state["options"][ix]))
    card_el.appendChild(supporting_el)

    def new_selection(_):
        state["selected"] = ix
        cb(None)

    add_event_listener(card_el, "click", new_selection)
    return card_el


def render_block(state, cb):
    block_el = document.createElement("div")
    block_el.className = "block-el"
    block_el.setAttribute("style", "margin-left: 10px; margin-right: 10px;")
    block_title = document.createElement("div")
    block_title.className = "block-title"
    # checkbox_el = (checkbox(state, cb), 4)
    # input_el = (numeric_input_el(state, cb), 8)
    # block_title.appendChild(make_cols([checkbox_el, input_el]))
    block_title.appendChild(checkbox(state, cb))
    block_el.appendChild(block_title)

    row_els = []
    for ix, _ in enumerate(state["options"]):
        row_els.append((block_option(ix, state, cb), 3))
    block_el.appendChild(make_cols(row_els))

    blank_el = document.createElement("div")
    custom_input_el = make_cols([(blank_el, 7), (numeric_input_el(state, cb), 5)])
    block_el.appendChild(custom_input_el)

    return block_el


def render_presets(state, callbacks):
    assert len(callbacks) == len(state["options"])
    block_el = document.createElement("div")
    block_el.className = "block-el"
    block_el.setAttribute("style", "margin-left: 10px; margin-right: 10px;")
    block_title = document.createElement("div")
    block_title.className = "block-title"
    block_title.appendChild(document.createTextNode(state["heading"]))
    block_el.appendChild(block_title)

    row_els = []
    for ix, _ in enumerate(state["options"]):
        row_els.append((block_option(ix, state, callbacks[ix]), 3))
    block_el.appendChild(make_cols(row_els))
    return block_el


def totalCO2(state):
    sum_co2 = 0
    for k, v in state.items():
        if v["enabled"]:
            sum_co2 += v["options"][v["selected"]].footprint
    sum_el = document.createElement("div")
    sum_el.appendChild(document.createTextNode(f"TinyML Total: {sum_co2:0.2f} kg CO2e"))
    return sum_el


def add_reference_points(footprint: dict):
    # static reference points
    footprint["system"].append("MacBook Pro (x1)")
    footprint["component"].append("reference")
    footprint["co2"].append(349)
    footprint["system"].append("Apple Watch S7 (x1)")
    footprint["component"].append("reference")
    footprint["co2"].append(34)


def plot_co2(state, extra_footprint, elem_id: str):
    footprint = {"system": [], "component": [], "co2": []}
    # footprint = {}
    footprint.update(extra_footprint)
    sum_co2 = 0
    for k, v in state["tinyml"].items():
        if v["enabled"]:
            footprint["system"].append("TinyML")
            footprint["component"].append(v["heading"])
            co2e = v["options"][v["selected"]].footprint
            footprint["co2"].append(co2e)
            sum_co2 += co2e
    for k, v in state["user_fields"].items():
        footprint["system"].append("TinyML")
        footprint["component"].append(k)
        footprint["co2"].append(v)
        sum_co2 += v
    add_reference_points(footprint)
    df = pd.DataFrame(footprint)
    fig = px.bar(
        df,
        x="system",
        y="co2",
        color="component",
        title="Embodied and Operational CO2 Footprint",
        log_y=True,
        labels=dict(system="System", co2="kg CO2e (log scale)")
    )
    fig.update_layout(autosize=False, width=400, height=700, margin=dict(l=0, r=0))
    # max_footprint = max(1.5, sum_co2)
    # fig.update_yaxes(range=[0, 160])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    plotly_render(graphJSON, elem_id)


def collapse_icon(elemid: str):
    icon_container = document.createElement("span")
    icon_container.setAttribute("style", "margin-left: 4px;")
    icon = document.createElement("span")
    icon.className = "icon material-icons mdl-color-text--grey-600"
    icon.setAttribute("id", elemid)
    icon.appendChild(document.createTextNode("settings"))
    # tooltip = document.createElement("span")
    # tooltip.className = "mdl-tooltip--right"
    # tooltip.setAttribute("for", elemid)
    # tooltip.appendChild(document.createTextNode("Collapse"))
    icon_container.appendChild(icon)
    # icon_container.appendChild(tooltip)
    componentHandler.upgradeElement(icon)
    # componentHandler.upgradeElement(tooltip)
    return icon_container


def make_note(key = None, custom: str = None):
    if not key:
        assert custom, "no note provided"
        note = custom
    elif key == "collapse":
        note =  "Note: click the gear icons to hide or expand configuration sections for TinyML"
    elif key == "mobilenet":
        note = "Note: MobileNetV1 CO₂ footprint uses ViT-Tiny CO₂ as a proxy value (Dodge et. al., FAccT '22)"
    note_el = document.createElement("span")
    note_el.className = "mdl-color-text--grey-600"
    note_el.setAttribute("style", "font-size: 0.6em;")
    note_el.appendChild(document.createTextNode(note))
    return note_el


def text_node(text: str):
    el = document.createElement("div")
    el.appendChild(document.createTextNode(text))
    return el


def _common_presets(tinyml):
    tinyml["casing"]["selected"] = 0
    tinyml["processor_type"]["selected"] = 1
    tinyml["pcb"]["selected"] = 1
    tinyml["power_supply"]["selected"] = 0
    tinyml["others"]["selected"] = 1
    tinyml["transport"]["selected"] = 1
    tinyml["ui"]["selected"] = 1
    tinyml["use_stage"]["selected"] = 0
    return


def yaml_section(state, cb):
    section = document.createElement("div")
    block_title = document.createElement("div")
    block_title.className = "block-title"
    block_title.appendChild(document.createTextNode("Custom TinyML CO2e Components"))
    section.appendChild(block_title)

    section.appendChild(text_node("You can add additional custom fields to the TinyML configuration by entering them (formatted as YAML) below"))


    # mdl text field
    textfield = document.createElement("div")
    textfield.className = "mdl-textfield mdl-js-textfield"
    textarea = document.createElement("textarea")
    textarea.className = "mdl-textfield__input"
    textarea.setAttribute("type", "text")
    textarea.setAttribute("rows", "3")
    textarea.setAttribute("id", "yaml-input")
    # if not empty
    if state["user_fields"]:
        textarea.value = yaml.dump(state["user_fields"], default_flow_style=False)
    textfield.appendChild(textarea)
    section.appendChild(textfield)
    componentHandler.upgradeElement(textfield)

    # calculate button
    def include_yaml(_):
        text = textarea.value
        try:
            dct = yaml.safe_load(text)
            for k, v in dct.items():
                if not isinstance(k, str) or not isinstance(v, (int, float)):
                    state["user_fields"] = {}
                    cb(_)
                    return
            state["user_fields"] = dct
            cb(_)
            return
        except:
            textarea.value = ""
            state["user_fields"] = {}
            cb(_)
            return
    section.appendChild(button("Add to Calculator", include_yaml))

    return section


class App:
    def __init__(self, state):
        assert "tinyml" in state
        self.state = state

    def preset_vision(self, _):
        tinyml = self.state["tinyml"]
        tinyml["ml_training"]["selected"] = 1
        tinyml["sensing"]["selected"] = 1
        _common_presets(tinyml)
        return self.build(None)

    def preset_anomaly(self, _):
        tinyml = self.state["tinyml"]
        tinyml["ml_training"]["selected"] = 0
        tinyml["sensing"]["selected"] = 0
        _common_presets(tinyml)
        return self.build(None)

    def collapse(self, state, key, _):
        state[key] = not state[key]
        return self.build(None)

    def render(self):
        app = document.getElementById("app")
        app.innerHTML = ""
        main_div = document.createElement("div")
        main_div.className = "container"
        app.appendChild(main_div)

        main_row = document.createElement("div")
        main_row.className = "row"
        main_div.appendChild(main_row)

        graph_container = document.createElement("div")
        graph_container.className = "col-lg-5"
        main_row.appendChild(graph_container)

        config_container = document.createElement("div")
        config_container.className = "col-lg-7"
        main_row.appendChild(config_container)

        # this doesnt need an inner container for collapsing
        preset_container = document.createElement("div")
        preset_container.className = "calcsection"
        # preset_container.appendChild(document.createTextNode("Presets"))
        preset_container.appendChild(
            render_presets(
                self.state["presets"], [self.preset_vision, self.preset_anomaly]
            )
        )
        config_container.appendChild(preset_container)

        tinyml_container = document.createElement("div")
        tinyml_container.className = "calcsection"
        tinyml_container.appendChild(document.createTextNode("TinyML"))

        ci_tiny = collapse_icon("tinyml_collapse")

        add_event_listener(
            ci_tiny, "click", partial(self.collapse, self.state["expanded"], "tinyml")
        )
        tinyml_container.appendChild(ci_tiny)
        config_container.appendChild(tinyml_container)

        tinyml_inner_container = document.createElement("div")
        tinyml_inner_container.setAttribute("id", "tinyml_configuration")
        if self.state["expanded"]["tinyml"]:
            tinyml_inner_container.style.display = "block"
        else:
            tinyml_inner_container.style.display = "none"
        tinyml_container.appendChild(tinyml_inner_container)


        for k, v in self.state["tinyml"].items():
            tinyml_inner_container.appendChild(render_block(v, self.build))

        yaml_container = document.createElement("div")
        yaml_container.className = "calcsection"
        yaml_container.appendChild(yaml_section(self.state, self.build))
        config_container.appendChild(yaml_container)

        config_container.appendChild(make_note("collapse"))
        config_container.appendChild(document.createElement("br"))
        config_container.appendChild(make_note("mobilenet"))

        # def mycb():
        #     print(self.state)
        #     self.state["ml_training"]["enabled"] = not self.state["ml_training"]["enabled"]
        #     self.build(None)
        # app.appendChild(button(mycb))
        # app.appendChild(document.createTextNode(f"{self.state}"))

        # graph_container.appendChild(text_node("TinyML vs. Traditional Server"))
        # graph_container.appendChild(text_node("Server Inferences/sec: 100 (placeholder)"))
        # graph_container.appendChild(text_node("TinyML Inferences/sec: 1 (placeholder)"))

        # print(f"{jload=}")
        # je = document.createTextNode(f"{jload}")
        # rje = document.createElement("div")
        # rje.appendChild(je)
        # graph_container.appendChild(rje)

        graph_el = document.createElement("div")
        co2_elem_id = "co2_graph"
        graph_el.setAttribute("id", co2_elem_id)
        graph_container.appendChild(graph_el)

        plot_co2(
            self.state, extra_footprint={}, elem_id=co2_elem_id
        )

        graph_container.appendChild(moreinfo())

    def build(self, event):
        # if event is not None:
        #     self.update_state()

        self.render()

def moreinfo():
    intro_text = "For more information on the usage of this TinyML CO₂ Footprint Calculator, please see our paper and documentation at "
    a_el = document.createElement("a")
    a_el.setAttribute("href", "https://github.com/harvard-edge/TinyML-Footprint")
    a_el.appendChild(document.createTextNode("github.com/harvard-edge/TinyML-Footprint"))
    info_el = document.createElement("div")
    info_el.appendChild(document.createTextNode(intro_text))
    info_el.appendChild(a_el)
    return info_el