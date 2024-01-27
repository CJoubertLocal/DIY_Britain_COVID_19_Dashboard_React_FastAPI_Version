const UpdateDatasetsButton = (explanationText, updateFunction, setterFunction, buttonText, buttonStyle) => (
    <>
        <p>
            {explanationText}
        </p>
        <button
            class={buttonStyle}
            onClick={() => {
                updateFunction(setterFunction)
            }}>{buttonText}</button>                
    </>
)

export default UpdateDatasetsButton
