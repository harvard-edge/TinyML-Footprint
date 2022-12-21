import elements as e

preset_state = dict(
    enabled=True,
    heading="Application Presets",
    docid="preset_id",
    options=[
        e.BlockOption(
            desc="Vision",
            footprint=0,
            act_desc="Classifier/Features",
        ),
        e.BlockOption(desc="Anomaly Detection", footprint=0, act_desc="Autoencoder"),
    ],
    selected=0,
)

tinyml_state = dict(
    ml_training=dict(
        enabled=True,
        heading="ML Training",
        docid="tinyml_training",
        options=[
            e.BlockOption(desc="DenseNet", footprint=0.1),
            e.BlockOption(desc="MobileNetV1", footprint=1.0),
        ],
        selected=1,
    ),
    casing=dict(
        enabled=True,
        heading="Casing",
        docid="tinyml_casing",
        options=[
            e.BlockOption(desc="ABS 200g/Steel 20g", footprint=0.04),
            e.BlockOption(desc="ABS 400g/Steel 80g", footprint=0.27),
            e.BlockOption(desc="ABS 700g/Steel 300g", footprint=0.63),
        ],
        selected=0,
    ),
    processor_type=dict(
        enabled=True,
        heading="Processing",
        docid="tinyml_processor_type",
        options=[
            e.BlockOption(desc="MCU 5 mm²", footprint=0.08),
            e.BlockOption(desc="MCU 10 mm²", footprint=0.17),
            e.BlockOption(desc="MCU 17 mm²", footprint=0.29),
        ],
        selected=1,
    ),
    pcb=dict(
        enabled=True,
        heading="PCB",
        docid="tinyml_pcb",
        options=[
            e.BlockOption(desc="HSL-0 small", footprint=0.13),
            e.BlockOption(desc="HSL-0 typical", footprint=0.16),
            e.BlockOption(desc="HSL-0 large", footprint=0.24),
        ],
        selected=1,
    ),
    power_supply=dict(
        enabled=True,
        heading="Power Supply",
        docid="tinyml_power_supply",
        options=[
            e.BlockOption(desc="Mains powered", footprint=0.52),
            e.BlockOption(desc="Li-ion battery (typical)", footprint=1.36),
            e.BlockOption(desc="Li-ion battery (large)", footprint=2.71),
        ],
        selected=0,
    ),
    sensing=dict(
        enabled=True,
        heading="Sensing",
        docid="tinyml_sensing",
        options=[
            e.BlockOption(desc="Electret Microphone", footprint=0.04),
            e.BlockOption(desc="30 mm² CMOS", footprint=0.77),
            e.BlockOption(desc="58 mm² CMOS", footprint=1.47),
        ],
        selected=1,
    ),
    others=dict(
        enabled=True,
        heading="Others",
        docid="tinyml_others",
        options=[
            e.BlockOption(desc="HSL-0 Best case", footprint=0.06),
            e.BlockOption(desc="HSL-0 Typical", footprint=0.11),
            e.BlockOption(desc="HSL-0 Worst case", footprint=0.14),
        ],
        selected=1,
    ),
    transport=dict(
        enabled=True,
        heading="Transport",
        docid="tinyml_transport",
        options=[
            e.BlockOption(desc="HSL-1 Best case", footprint=0.18),
            e.BlockOption(desc="HSL-1 Typical", footprint=0.4),
            e.BlockOption(desc="HSL-1 Worst case", footprint=1.35),
        ],
        selected=1,
    ),
    ui=dict(
        enabled=True,
        heading="Indicator LED UI",
        docid="tinyml_ui",
        options=[
            e.BlockOption(desc="1 LED", footprint=0.03),
            e.BlockOption(desc="2 LEDs", footprint=0.06),
            e.BlockOption(desc="4 LEDs", footprint=0.12),
        ],
        selected=1,
    ),
    use_stage=dict(
        enabled=True,
        heading="Use-Stage",
        docid="tinyml_use_stage",
        options=[
            e.BlockOption(desc="Continuous 1mW", footprint=0.01),
        ],
        selected=0,
    ),
)


def main():
    for key in tinyml_state.keys():
        tinyml_state[key]["options"].append(e.BlockOption(desc="Custom", footprint=0.0))
    app = e.App(
        dict(
            presets=preset_state,
            user_fields={},
            tinyml=tinyml_state,
            expanded=dict(tinyml=True),
        )
    )
    app.preset_vision(None)


main()
