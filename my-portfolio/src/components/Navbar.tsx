type Props = {
    name: string;
};

export default function Navbar({ name }: Props) {
    return (
        <nav style={{ padding: "1rem", borderBottom: "1px solid #ccc" }}>
            <h2>{name}</h2>
        </nav>
    );
}