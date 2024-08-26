# from sqlalchemy import text
#
#
# class LiveRecentUpdater:
#     function_sql = """
#         CREATE OR REPLACE FUNCTION update_live_recent()
#         RETURNS TRIGGER AS $$
#         BEGIN
#             -- Update the most recent data in live_recent when new data is inserted into live_data
#             UPDATE live_recent
#             SET current = NEW.current,
#                 voltage = NEW.voltage,
#                 created_at = NEW.created_at
#             WHERE machine_id = NEW.machine_id;
#
#             -- If no data was updated (no match found), insert a new record into live_recent
#             IF NOT FOUND THEN
#                 INSERT INTO live_recent (current, voltage, created_at, machine_id)
#                 VALUES (NEW.current, NEW.voltage, NEW.created_at, NEW.machine_id);
#             END IF;
#
#             RETURN NEW;
#         END;
#         $$ LANGUAGE plpgsql;
#     """
#
#     trigger_insert_sql = """
#         CREATE TRIGGER after_insert_live_data
#         AFTER INSERT ON live_data
#         FOR EACH ROW
#         EXECUTE FUNCTION update_live_recent();
#     """
#
#     trigger_update_sql = """
#         CREATE TRIGGER after_update_live_data
#         AFTER UPDATE ON live_data
#         FOR EACH ROW
#         EXECUTE FUNCTION update_live_recent();
#     """
#
#     def __init__(self, engine):
#         self.engine = engine
#
#     def setup_triggers(self):
#         with self.engine.connect() as connection:
#             # Create the function
#             connection.execute(text(self.function_sql))
#
#             # Create the triggers
#             connection.execute(text(self.trigger_insert_sql))
#             connection.execute(text(self.trigger_update_sql))
