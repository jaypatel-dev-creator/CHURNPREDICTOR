import "./SectionHeader.css"
const SectionHeader = ({ title }) => {
    return (
        <div className="section-header">
            <h3 className="section-title">{title}</h3>
            <div className="section-divider" />
        </div>
    )
}

export default SectionHeader